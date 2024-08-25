# Parx_Project
## Contents
- [Overview](#overview)
  - [Purpose](#purpose)
  - [How It Helps ParkPrescriptions.ca](#how-it-helps-parkprescriptionsca)
- [Demo and Live Website](#demo-and-live-website)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Key Features](#key-features)
  - [Admin View](#admin-view)
  - [Patient and Prescriber Interaction](#patient-and-prescriber-interaction)
  - [Green Resources](#green-resources)
  - [Security and Permissions](#security-and-permissions)
- [Login Details for Demo Accounts](#login-details-for-demo-accounts)
- [Team Members](#team-members)
- [Installation and Setup](#installation-and-setup)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
## Overview
![image](https://github.com/user-attachments/assets/342dfbf5-5c2a-41d3-ba0e-05fcc1602ef3)

**NotParx** is a prescription platform designed to enhance the functionality of [ParkPrescriptions.ca](https://www.parkprescriptions.ca/) and developed at the request of PaRx as part of the CSCC01 course at UTSC (Introduction to Software Engineering). This project interfaces with 10 Canadian medical databases in real-time, allowing healthcare professionals to issue park prescriptions efficiently. The platform is built with scalability, availability, and ease of use in mind, offering a seamless experience for both administrators and users.

### Purpose

The primary goal of NotParx is to streamline the process of issuing park prescriptions, making it easier for healthcare professionals to encourage outdoor activities for their patients. By integrating real-time data and providing a robust interface, NotParx supports the mission of ParkPrescriptions.ca in promoting the health benefits of nature through park prescriptions.

### How It Helps ParkPrescriptions.ca

NotParx provides a dynamic interface that supports the goals of ParkPrescriptions.ca by:
- **Real-Time Data Processing**: Integrating real-time data from multiple Canadian medical databases to ensure accuracy and speed.
- **Scalable Infrastructure**: Utilizing cloud technologies like Azure, Azure Functions, and MongoDB Atlas to ensure scalability and availability.
- **Enhanced User Experience**: Offering a user-friendly interface for coordinators, assistants, prescribers, and patients to manage prescriptions effectively.

## Demo and Live Website

[Video Demo](https://www.youtube.com/watch?v=sij9cLY_qe0)

Please note that due to resource constraints, all backend and Azure-dependent functionalities are removed in the demo.

The front-end of NotParx is live and can be accessed at [NotParx Demo-Live Website](https://c01notparx.netlify.app/), but it is unlikely that you would be able to log in at this time. 

## Technology Stack
- **Frontend**: Built with ReactJS for a dynamic and responsive user interface.
- **Backend**: Powered by Django, offering scalable microservice integration.
- **Data Integration**: Real-time data scraping using Azure Functions and Python web-scraping for over 10 Canadian medical databases.
- **Infrastructure**: Azure App Services, Azure Blob Storage, and Azure Functions. MongoDB within AWS cloud infrastructure, optimized for performance and scalability.
- **Deployment**: CI/CD using Github Actions and Azure.

## System Architecture
![System Architecture Diagram](deliverable4/Updated%20Software%20Architecture%20Diagram.png)

## Key Features

### Admin View
- **CSV Management**:
  - Upload and process CSV files containing prescriber data.
  - Automatically prevents duplication of records and handles errors efficiently.
  - Download processed CSV files directly from the interface.

- **Profile Management**:
  - View all processed prescribers and patients in a centralized location.
  - Automatically generate unique codes for new prescribers.
  - Easily match prescribers with patients and manage their profiles.

- **Prescription Handling**:
  - Admins can create, update, and manage prescriptions.
  - Prescription statuses are automatically synced across the platform.
  - Download prescription PDFs, which include all necessary details, directly from the platform.

### Patient and Prescriber Interaction
- **Account Creation**:
  - Seamlessly create accounts for both prescribers and patients using unique codes.
  - The system includes error handling to guide users through the process.
  - Manage account information, including optional details like addresses.

- **Prescription Management**:
  - Prescribers can assign prescriptions to patients with real-time logging.
  - Patients can view their prescriptions and update their information as needed.
  - Status updates are reflected immediately, and prescriptions can be downloaded once they are logged and matched.

- **Required Actions**:
  - The platform flags accounts with missing or incorrect information, prompting users to update their details.
  - Notifications for required actions are prominently displayed to ensure compliance.

### Green Resources
- **Interactive Map**:
  - Explore a wide range of green spaces and outdoor activities across Canada.
  - Filter by resource type (e.g., parks, gardens, dog parks) to find exactly what you’re looking for.
  - Location-based search allows users to find green resources near their current location.

- **Custom Icons**:
  - Each type of green resource is represented by a unique icon for easy identification.
  - The map dynamically updates based on the selected filters and location.

### Security and Permissions
- **Role-Based Access Control**:
  - Coordinators, assistants, prescribers, and patients each have specific access levels.
  - The platform enforces strict access controls to protect sensitive information.
  - Unauthorized attempts to access restricted areas are automatically redirected to appropriate pages.

## Login Details for Demo Accounts

The following credentials were used for demo admin accounts, but are not currently available:

- **Coordinator Account**:
  - Username: `Coordinator`
  - Password: `CoordPassword`

- **Assistant Account**:
  - Username: `Assistant`
  - Password: `AssistPassword`

Prescriber and patient accounts can be created directly through the interface, so no demo account details are provided for these roles.

## Team Members

NotParx was developed by:

- Dmitiry Prokopchuk
- Shreyas Rao
- Alankrit Verma
- Katarina Sotic
- Connor Musson
- Cindy Ji

## Installation and Setup

To run NotParx locally or in your environment, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/NotParx.git
    cd NotParx
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**:
    - Configure your cloud environment and database settings in a `.env` file.

4. **Run the Application**:
    ```bash
    python manage.py runserver
    ```

5. **Access the Application**:
    - Visit `http://localhost:8000` in your browser to access the platform.

## Contributing

This project is generally closed for contributions, but feel free to contact the team. 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to CSCC01 Winter 2024 Group 2 for their contributions to the project.
- Data sources from OpenStreetMaps for green resources.
