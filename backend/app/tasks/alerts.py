"""
Alert tasks - Check and trigger user alerts
"""
from celery import shared_task
from loguru import logger
from datetime import datetime

from app.core.database import SessionLocal
from app.models import Alert, Company, StockPrice, Ratio


@shared_task(name="app.tasks.alerts.check_all_alerts")
def check_all_alerts():
    """Check all active alerts and trigger if conditions are met"""
    logger.info("Checking all active alerts")

    db = SessionLocal()
    try:
        # Get all active, non-triggered alerts
        alerts = db.query(Alert).filter(
            Alert.is_active == True,
            Alert.is_triggered == False
        ).all()

        logger.info(f"Checking {len(alerts)} active alerts")

        triggered_count = 0

        for alert in alerts:
            try:
                if check_alert_condition(alert, db):
                    # Mark as triggered
                    alert.is_triggered = True
                    alert.triggered_at = datetime.utcnow()

                    # Send notification (email, push, etc.)
                    send_alert_notification(alert, db)

                    triggered_count += 1

            except Exception as e:
                logger.error(f"Error checking alert {alert.id}: {e}")
                continue

        db.commit()
        logger.info(f"Triggered {triggered_count} alerts")

        return {'checked': len(alerts), 'triggered': triggered_count}

    except Exception as e:
        logger.error(f"Error in check_all_alerts task: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def check_alert_condition(alert: Alert, db) -> bool:
    """
    Check if alert condition is met

    Args:
        alert: Alert object
        db: Database session

    Returns:
        True if condition is met
    """
    try:
        if alert.alert_type == "price_above" or alert.alert_type == "price_below":
            # Check price condition
            latest_price = db.query(StockPrice).filter(
                StockPrice.company_id == alert.company_id
            ).order_by(StockPrice.date.desc()).first()

            if not latest_price:
                return False

            current_price = latest_price.close

            if alert.alert_type == "price_above" and current_price > alert.condition_value:
                alert.triggered_value = current_price
                return True
            elif alert.alert_type == "price_below" and current_price < alert.condition_value:
                alert.triggered_value = current_price
                return True

        elif alert.condition_field and alert.condition_operator and alert.condition_value:
            # Check ratio-based condition
            latest_ratio = db.query(Ratio).filter(
                Ratio.company_id == alert.company_id
            ).order_by(Ratio.period_end.desc()).first()

            if not latest_ratio:
                return False

            field_value = getattr(latest_ratio, alert.condition_field, None)

            if field_value is None:
                return False

            # Check operator
            if alert.condition_operator == ">" and field_value > alert.condition_value:
                alert.triggered_value = field_value
                return True
            elif alert.condition_operator == "<" and field_value < alert.condition_value:
                alert.triggered_value = field_value
                return True
            elif alert.condition_operator == ">=" and field_value >= alert.condition_value:
                alert.triggered_value = field_value
                return True
            elif alert.condition_operator == "<=" and field_value <= alert.condition_value:
                alert.triggered_value = field_value
                return True
            elif alert.condition_operator == "==" and field_value == alert.condition_value:
                alert.triggered_value = field_value
                return True

        return False

    except Exception as e:
        logger.error(f"Error checking condition for alert {alert.id}: {e}")
        return False


def send_alert_notification(alert: Alert, db):
    """
    Send notification for triggered alert

    Args:
        alert: Alert object
        db: Database session
    """
    try:
        # Get company info
        company = db.query(Company).filter(Company.id == alert.company_id).first()

        if not company:
            return

        message = f"Alert triggered for {company.name} ({company.symbol}): {alert.message or alert.title}"

        logger.info(f"Alert notification: {message}")

        # Here you would:
        # 1. Send email if alert.notify_email
        # 2. Send push notification if alert.notify_app
        # 3. Log to notification table

        # Placeholder implementation
        if alert.notify_email:
            # send_email(alert.user.email, alert.title, message)
            pass

        if alert.notify_app:
            # send_push_notification(alert.user_id, message)
            pass

    except Exception as e:
        logger.error(f"Error sending notification for alert {alert.id}: {e}")
