# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime

class HrPayslip(models.Model):
    _inherit = "hr.payslip"
    
    @api.model
    def prepare_leave_days(self, employee, leaves, payslip, date_from, date_to):
        
        domaine = [
            ('employee_id', '=', employee.id),
        ]
        leaves = self.env['hr.leave'].search(domaine)
        number_of_hours = 0
        number_of_days = 0
        for leave in leaves:
            t = leave.date_from
            date = t.date()
            if date_from <= date <= date_to:
                number_of_hours += leave.number_of_hours_display
                number_of_days += leave.number_of_days
                work_entry = leave.holiday_status_id.work_entry_type_id
                paid_amount = self._get_contract_wage()
                unpaid_work_entry_types = self.struct_id.unpaid_work_entry_type_ids.ids

                work_hours = payslip.contract_id._get_work_hours(date_from, date_to)
                total_hours = sum(work_hours.values())
                is_paid = work_entry.id not in unpaid_work_entry_types
                if payslip.contract_id.wage_type == "hourly":
                    amount = payslip.contract_id.hourly_wage * number_of_hours
                else:
                    amount = number_of_hours * paid_amount / total_hours if is_paid else 0

                
      
        # Get formated date from the leaves
        #date_from_formated = overtimes.start_date
                    
        if number_of_hours > 0 or number_of_days > 0:

            return{
                'name': _('Leaves'),
                'sequence': work_entry.sequence,
                'work_entry_type_id': work_entry.id,
                'number_of_hours': number_of_hours,
                'number_of_days':number_of_days,
                'contract_id': payslip.contract_id.id,
                'imported_from_leave': True,
                'payslip_id': payslip.id,
                'amount': amount
            }
        return False


    def _leaves_mapping(self, leaves, payslip, date_from, date_to):
        """This function takes timesheet objects imported from the timesheet
        module and creates a dict of worked days to be created in the payslip.
        """
        # Create one worked days record for each timesheet sheet
        for leave in leaves:
            worked_days_data = self.prepare_leave_days(
                payslip.employee_id, leave, payslip,date_from, date_to)
        if worked_days_data:
            self.env['hr.payslip.worked_days'].create(worked_days_data)



    def _check_contract(self):
        """Contract is not required field for payslips, yet it is for
        payslips.worked_days."""
        for payslip in self:
            if not payslip.contract_id:
                raise UserError(
                    _("Contract is not defined for one or more payslips."),
                )
                
    @api.model
    def get_leaves_from_employee(self, employee, date_from, date_to):
        criteria = [
            ('date_from', '>=', date_from),
            ('date_to', '<=', date_to),
            ('state', 'in', ('confirm','validate','validate1')),
            ('employee_id', '=', employee.id),
        ]
        leave_model = self.env['hr.leave']
        leaves = leave_model.search(criteria)
        if not leaves:
            raise UserError(
                _("Sorry, but there is no approved Leaves for the \
                entire Payslip period for user %s") % employee.name,
            )
        return leaves
    
    

    def import_leaves_days(self):
        """This method retreives the employee's leaves for a payslip period
        and creates worked days records from the imported timesheets
        """
        self._check_contract()
        for payslip in self:
            date_from = payslip.date_from
            date_to = payslip.date_to

            # Delete old imported worked_days
            # The reason to delete these records is that the user may make
            # corrections to his timesheets and then reimport these.
            self.env['hr.payslip.worked_days'].search(
                [('payslip_id', '=', payslip.id),
                 ('imported_from_leave', '=', True)]).unlink()

            # get timesheet sheets of employee
            leaves = self.get_leaves_from_employee(
                payslip.employee_id, date_from, date_to)
            # The reason to call this method is for other modules to modify it.
            self._leaves_mapping(leaves, payslip, date_from, date_to)