"""
Patron Routes - Patron related endpoints
"""

from flask import Blueprint, render_template, request, flash
from library_service import get_patron_status_report

# Define blueprint for patron-related routes
patron_bp = Blueprint('patron', __name__)

@patron_bp.route('/patron', methods=['GET', 'POST'])
def patron_status():
    if request.method == 'GET':
        return render_template('patron.html', patron=None, report=None)

    patron_id = request.form.get('patron_id', '').strip()

    if not patron_id.isdigit() or len(patron_id) != 6:
        flash('Invalid Patron ID. Must be exactly 6 digits.', 'error')
        return render_template('patron.html', patron=None, report=None)

    report = get_patron_status_report(patron_id)

    if not report or report.get("num_currently_borrowed", 0) == 0 and not report.get("borrowing_history"):
        flash(f'No records found for Patron ID {patron_id}.', 'error')
        return render_template('patron.html', patron=patron_id, report=None)

    return render_template('patron.html', patron=patron_id, report=report)
