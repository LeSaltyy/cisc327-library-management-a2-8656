import pytest
from unittest.mock import Mock
from services.library_service import pay_late_fees, refund_late_fee_payment
from services.payment_service import PaymentGateway

@pytest.fixture
def stub_database_functions(mocker):
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={"fee_amount": 10.0, "days_overdue": 2, "status": "Overdue"}
    )
    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value={'id': 1, 'title': 'Stub Book'}
    )

def test_late_success(stub_database_functions):
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Payment processed")

    success, message, txn_id = pay_late_fees("123456", 1, payment_gateway=mock_gateway)

    mock_gateway.process_payment.assert_called_once_with(
        patron_id="123456",
        amount=10.0,
        description="Late fees for 'Stub Book'"
    )
    assert success is True
    assert txn_id == "txn_123"
    assert "Payment successful" in message

def test_payment_declined(stub_database_functions):
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, "", "Payment declined")

    success, message, txn_id = pay_late_fees("123456", 1, payment_gateway=mock_gateway)

    mock_gateway.process_payment.assert_called_once()
    assert success is False
    assert txn_id is None
    assert "Payment failed" in message

def test_invalid_patron(stub_database_functions):
    mock_gateway = Mock(spec=PaymentGateway)

    success, message, txn_id = pay_late_fees("123", 1, payment_gateway=mock_gateway)

    mock_gateway.process_payment.assert_not_called()
    assert success is False
    assert txn_id is None
    assert "Invalid patron ID" in message

def test_refund_success():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund successful")

    success, message = refund_late_fee_payment("txn_123", 10, payment_gateway=mock_gateway)

    mock_gateway.refund_payment.assert_called_once_with("txn_123", 10)
    assert success is True
    assert message == "Refund successful"

def test_invalid_transaction_id():
    mock_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment("invalid_txn", 10, payment_gateway=mock_gateway)

    mock_gateway.refund_payment.assert_not_called()
    assert success is False
    assert "Invalid transaction ID" in message

def test_refund_invalid_amount():
    mock_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment("txn_123", 20, payment_gateway=mock_gateway)
    mock_gateway.refund_payment.assert_not_called()
    assert success is False

def test_gateway_process_payment_branches(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda x: None)
    gateway = PaymentGateway()

    # Invalid amount <= 0
    success, txn_id, msg = gateway.process_payment("123456", 0)
    assert not success
    assert txn_id == ""
    assert "Invalid amount" in msg

    # Amount exceeds 1000
    success, txn_id, msg = gateway.process_payment("123456", 5000)
    assert not success
    assert txn_id == ""
    assert "exceeds limit" in msg

    # Invalid patron ID
    success, txn_id, msg = gateway.process_payment("123", 50)
    assert not success
    assert txn_id == ""
    assert "Invalid patron ID" in msg

    # Valid success
    success, txn_id, msg = gateway.process_payment("123456", 50)
    assert success
    assert txn_id.startswith("txn_")
    assert "processed successfully" in msg

def test_gateway_refund_payment_branches(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda x: None)
    gateway = PaymentGateway()

    # Invalid transaction
    success, msg = gateway.refund_payment("", 10)
    assert not success
    assert "Invalid transaction" in msg

    # Invalid amount
    success, msg = gateway.refund_payment("txn_123456", 0)
    assert not success
    assert "Invalid refund amount" in msg

    # Valid refund
    success, msg = gateway.refund_payment("txn_123456", 10)
    assert success
    assert "Refund of $10.00" in msg

def test_gateway_verify_payment_status_branches(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda x: None)
    gateway = PaymentGateway()

    # Invalid transaction
    result = gateway.verify_payment_status("")
    assert result["status"] == "not_found"

    # Valid transaction
    result = gateway.verify_payment_status("txn_123456")
    assert result["status"] == "completed"
    assert result["transaction_id"] == "txn_123456"
