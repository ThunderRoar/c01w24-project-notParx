from fpdf import FPDF
from datetime import datetime

# Define a class that inherits from FPDF which is used to create the PDF
class PDF(FPDF):
    def footer(self):
        # Add a footer with the Prescription #, Date, and Patient's Initials
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        # Replace the en dash with a simple hyphen
        self.cell(0, 10, f'Prescription #: {self.prescription_code} - {self.current_date} - {self.patient_initials}', 0, 0, 'C')

# Function to create the PDF document
def create_pdf(name, activity_plan, prescription_code, patient_initials):
    # Create an instance of the PDF class
    pdf = PDF()
    pdf.prescription_code = prescription_code
    pdf.current_date = datetime.now().strftime('%y%m%d')  # Current date in YYMMDD format
    pdf.patient_initials = patient_initials
    
    # Add a page to the PDF
    pdf.add_page()
    
    # Set the title and author of the document
    pdf.set_title("Outdoor Activity Plan")
    pdf.set_author('Health Professional')

    # Add name to the PDF
    pdf.set_font('Helvetica', '', 12)
    pdf.ln(10)  # Move 10 down
    pdf.cell(0, 10, f'Name {name}')

    # Add date to the PDF
    pdf.cell(0, 10, f'Date {pdf.current_date}', new_x="LMARGIN", new_y="NEXT")
    
    # Add Outdoor Activity Plan
    pdf.multi_cell(0, 10, f'My Outdoor Activity Plan:\n{activity_plan}')
    
    # Line break before the footer content
    pdf.ln(50)  # Move 50 down to simulate the space before the footer

    # Add a line for Health Professional's Signature
    pdf.cell(0, 10, '________________________________________', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, "Health Professional's Signature", new_x="LMARGIN", new_y="NEXT")
    
    # Output the PDF to a file
    pdf.output('Outdoor_Activity_Plan.pdf')

# Uncomment the below line to run the function with example data
create_pdf('John Doe', 'Walking in the park', 'RX123456', 'JD')
