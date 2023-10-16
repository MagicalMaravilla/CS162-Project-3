import datetime
import re
import logging

logging.basicConfig(filename='secure_password_system.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

class SecurePasswordSystemG:
    def __init__(self):
        self.password = None
        self.username = None
        self.locked_until = None
        self.failed_attempts = 0
        self.guest_expiration = None
        self.guest_attempts = 0
        self.guest_password = '1969'
        logging.info('SecurePasswordSystemG Initialized.')

    def set_initial_username(self, username_input):
        username_pattern = re.compile(r'[\w\s]{1,20}$')
        try:
            username = username_input.strip()
            if not username:
                self.username = "User123"
                return f'Username cannot be empty. Using default username "user123". Welcome {username}!'
            elif username_pattern.match(username):
                self.username = username
                return f'Welcome {self.username}!'
            else:
                return 'Invalid username. Ensure it\'s within 20 character letters, numbers, and symbols'
        except Exception as e:
            logging.error(f"An error occurred while setting username: {e}")
            return 'An unexpected error occurred. Please try again.'

    def reset_username(self, confirmation, current_password):
        try:
            if confirmation.lower() != 'yes':
                return 'Username reset cancelled.'
            if current_password != self.password:
                return 'Incorrect password. Username reset cancelled.'
            return 'Please set new user name.'
        except Exception as e:
            logging.error(f'An error occurred while resetting username: {e}')
            return 'An unexpected error occurred. Please try again.'

    def set_initial_password(self, password_input):
        try:
            password = password_input.strip()
            if not password:
                self.password = '1776'
                return 'Password cannot be empty. Using default password for this specific device to "1776".'
            elif len(password) == 4 and password.isdigit():
                self.password = password
                return f'Password set successfully, welcome {self.username} to Secure Home Inc family. Your safety is our' \
                       f'number one concern.'
            else:
                return 'Invalid input. Please enter a 4-digit numeric password'
        except Exception as e:
            logging.error(f"An error occurred while setting password: {e}")
            return 'An unexpected error occurred. Please try again. '

    def reset_password(self, confirmation):
        if confirmation.lower() != 'yes':
            return 'Password reset cancelled.'
        return 'Please set a new password.'

    def verify_password(self, enter_password):
        max_attempts = 3
        if self.locked_until and datetime.datetime.now() < self.locked_until:
            return f'Account is locked until {self.locked_until}. Please wait, or contact  customer support.'
        if enter_password == self.password:
            self.failed_attempts = 0
            self.locked_until = None
            logging.info(f'Successful login by {self.username}.')
            return 'Access granted'
        else:
            self.failed_attempts += 1
            remaining_attempts = max_attempts - self.failed_attempts
            if remaining_attempts > 0:
                logging.warning(f'Failed login attempt {self.failed_attempts} by {self.username}')
                return f'Incorrect password. Try again. You have {remaining_attempts} attempts left'
            self.check_failed_attempts()
            return f'Multiple failed attempts detected, {self.username}! System locked until {self.locked_until}.'

    def check_failed_attempts(self):
        try:
            if self.failed_attempts >= 3:
                self.locked_until = datetime.datetime.now() + datetime.timedelta(hours=1)
        except Exception as e:
            logging.error(f'An error occurred while checking failed attempts: {e}')

    def set_guest_access(self, duration, time_choice, time_of_day=None):
        try:
            if not 1 <= duration <= 31:
                return 'Invalid duration. Please enter a value between 1 and 31.'
            if time_choice.lower().strip() == 'yes':
                match = re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', time_of_day)
                if not match:
                    return 'Invalid time format. Please use the HH:MM in 24 hour format.'
            elif time_choice.lower().strip() == 'no':
                time_of_day = datetime.datetime.now().strftime('%H:%M')
            else:
                return 'Please respond with "yes" or "no".'
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=duration)
            hour, minute = map(int, time_of_day.split(':'))
            self.guest_expiration = expiration_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            return f'Guest access granted until {self.guest_expiration}'
        except Exception as e:
            logging.error(f'An error occurred while setting guest access: {e}')
            return 'An unexpected error occurred. Please try again.'

    def verify_guest_access(self, guest_password):
        current_time = datetime.datetime.now()
        if not self.guest_expiration or current_time > self.guest_expiration:
            return 'Guest access expired or not set.'
        if current_time.hour >= 0 and current_time.hour < 6:
            return 'Access restricted during nighttime (12AM - 6 AM).'
        if self.guest_attempts >= 10:
            return 'Too many failed attempts. Guest access locked.'
        if guest_password == self.guest_password:
            logging.info(f'Guest accessed at {current_time}.')
            return 'Guest access granted.'
        else:
            self.guest_attempts += 1
            return f'Incorrect password. You have {10 - self.guest_attempts} attempts left.'

    def owner_override(self, owner_password):
        if owner_password == self.password:
            logging.info(f'Owner override at {datetime.datetime.now()}.')
            return 'Owner Override successful. Access granted.'
        else:
            return 'Incorrect owner password. Access Denied'

    def set_guest_password(self, password_input):
        try:
            password = password_input.strip()
            if not password:
                return 'Guest password cannot be empty.'
            elif len(password) == 4 and password.isdigit():
                self.guest_password = password
                return f'Guest password set successfully. Please share it with your guest responsibly.'
            else:
                return 'Invalid input. Please enter a 4-digit numeric password for the guest.'
        except Exception as e:
            logging.error(f"An error occurred while setting guest password: {e}")
            return 'An unexpected error occurred. Please try again.'

    def change_guest_password(self, owner_password, new_guest_password):
        if owner_password!= self.password:
            return 'Incorrect owner password. Access denied.'
        try:
            if len(new_guest_password) == 4 and new_guest_password.isdigit():
                self.guest_password = new_guest_password
                return f'Guest password changed successfully. Please share it with your guest responsibly.'
            else:
                return 'Invalid input. Please enter a 4-digit numeric password for the guest.'
        except Exception as e:
            logging.error(f"An error occurred while changing guest password: {e}")
            return 'An unexpected error occurred. Please try again.'

    def deactivate_guest_access(self, owner_password):
        if owner_password != self.password:
            return 'Incorrect owner password. Access Denied.'
        self.guest_expiration = None
        return 'Guest access deactivated successfully.'

    def check_system_status(self):
        current_time = datetime.datetime.now()
        status = {
            'username':self.username,
            'locked_until':self.locked_until,
            'failed_attempts':self.failed_attempts,
            'guest_expiration':self.guest_expiration,
            'guest_attempts':self.guest_attempts,
            'current_time': current_time
        }
        return status



