from fpdf import FPDF
from fpdf import YPos
from fpdf import XPos
from datetime import datetime
import os

# Define a class that inherits from FPDF which is used to create the PDF
class PDF(FPDF):       
    def add_content(self, name, activity_plan, prescriber_code, patient_initials):
        # Store data for use in footer
        self.prescriber_code = prescriber_code
        self.current_date = datetime.now().strftime('%y%m%d')
        self.patient_initials = patient_initials
        
        # Add name
        self.set_font('Helvetica', '', 12)
        self.cell(text=f'Patient: {name}', align='L', w = 0, h = 10, border = 0)
        self.ln(10)

        # Add date
        self.cell(text=f'Date: {self.current_date}', align='L', w = 0, h = 10, border = 0)
        self.ln(20)

        # Add Outdoor Activity Plan
        self.cell(text='Outdoor Activity Plan:', align='L', w = 0, h = 10, border = 0)
        self.ln(10)
        self.multi_cell(text=f"{activity_plan}", align='C', w = 0, h = 10, border = 0)

        # Simulate space before the footer
        self.ln(180)

        # Add a line for Health Professional's Signature
        self.cell(0, 10, '________________________________________')
        self.ln(10)
        self.cell(text="Health Professional's Signature", align='L', w = 0, h = 10, border = 0)
        self.ln(10) 
        page_width = self.w - 2 * self.l_margin  # Calculate the available page width
        box_width = page_width / 3  # Divide the page width by three for the three boxes

        # Draw the first box for the prescription number
        self.cell(w=box_width, h=10, text=f'Prescriber #: {self.prescriber_code}', border=0, align='L', fill=False, new_x=XPos.RIGHT, new_y=YPos.TOP)

        # Draw the second box for the date
        self.cell(w=box_width, h=10, text=f'Date: {self.current_date}', border=0, align='L', fill=False, new_x=XPos.RIGHT, new_y=YPos.TOP)

        # Draw the third box for the patient's initials
        self.cell(w=box_width, h=10, text=f'Patient Initials: {self.patient_initials}', border=0, align='L', fill=False, new_x=XPos.RIGHT, new_y=YPos.TOP)

        self.ln(10)


# Function to create the PDF document
def create_pdf(name, activity_plan, prescriber_code, patient_initials):
    # Create an instance of the PDF class
    pdf = PDF()
    
    # Add a page to the PDF
    pdf.add_page()
    
    # Set the title and author of the document
    pdf.set_title("Outdoor Activity Plan")
    pdf.set_author('Health Professional')

    # Add the content to the PDF
    pdf.add_content(name, activity_plan, prescriber_code, patient_initials)
    return pdf
    
# create_pdf('Shreyas Rao', 'Play cricket with Alankrit', 'ABC123', 'SR')