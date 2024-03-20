# Correcting the deprecation warning by removing the 'ln' parameter and managing new line manually

from fpdf import FPDF
from datetime import datetime

# Define a class that inherits from FPDF which is used to create the PDF
class PDF(FPDF):
    def footer(self):
        # Ensure the footer is at the bottom of the page
        self.set_y(-15)
        # Set the font for the footer
        self.set_font('Helvetica', 'I', 8)
        # Add a footer with the Prescription #, Date, and Patient's Initials
        self.cell(0, 10, 'Prescription #: {self.prescription_code} - {self.current_date} - {self.patient_initials}', 0, 0, 'C')

    def add_content(self, name, activity_plan, prescription_code, patient_initials):
        # Store data for use in footer
        self.prescription_code = prescription_code
        self.current_date = datetime.now().strftime('%y%m%d')  # Current date in YYMMDD format
        self.patient_initials = patient_initials
        
        # Add name
        self.set_font('Helvetica', '', 12)
        self.cell(0, 10, f'Name {name}')
        self.ln(10)

        # Add date
        self.cell(0, 10, f'Date {self.current_date}')
        self.ln(10)
        
        # Add Outdoor Activity Plan
        self.multi_cell(0, 10, f'My Outdoor Activity Plan:\n{activity_plan}')
        self.ln(10)  # Add a line break after the activity plan

        # Simulate space before the footer
        self.ln(50)

        # Add a line for Health Professional's Signature
        self.cell(0, 10, '________________________________________')
        self.ln(10)
        self.cell(0, 10, "Health Professional's Signature")
        self.ln(10)  # Ensure there's a line break after the signature

# Function to create the PDF document
def create_pdf(name, activity_plan, prescription_code, patient_initials):
    # Create an instance of the PDF class
    pdf = PDF()
    
    # Add a page to the PDF
    pdf.add_page()
    
    # Set the title and author of the document
    pdf.set_title("Outdoor Activity Plan")
    pdf.set_author('Health Professional')

    # Add the content to the PDF
    pdf.add_content(name, activity_plan, prescription_code, patient_initials)
    
    # Save the PDF to a file
    pdf.output('/mnt/data/Outdoor_Activity_Plan.pdf')

# Uncomment the below line to run the function with example data
# create_pdf('John Doe', 'Walking in the park', 'RX123456', 'JD')
