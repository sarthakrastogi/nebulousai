from all_abilities import send_email

class PointOfContact:
    def __init__(self, point_of_contact_name, communication_mode, communication_address) -> None:
        self.point_of_contact_name = point_of_contact_name
        self.communication_address = communication_address
        self.communication_mode = communication_mode

    def communicate(self, name, message_subject, message_body):
        if self.communication_mode == "email":
            return send_email(name=name,
                              email_address=self.communication_address,
                              email_subject=message_subject,
                              email_body=message_body)
