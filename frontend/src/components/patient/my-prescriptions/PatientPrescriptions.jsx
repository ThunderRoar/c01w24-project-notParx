import './PatientPrescriptions.scss';
import PatientAddPrescription from './PatientAddPrescription/PatientAddPrescription';

import * as React from 'react';
import ReactPopup from 'reactjs-popup';
import { Button } from '@mui/material';
import TablePagination from '@mui/material/TablePagination';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';

const PatientPrescriptions = () => {
    const sampleData = [
        { provDocID: 'ON-JB001', patientInitials: 'OW', date: '22 Mar 2024', discoveryPass: true, status: 'Logged' },
    ];
  
    const prescriptionColumns = [ // Sample columns - add depending on what api returns
        { id: 'provDocID', label: 'Provider Code' },
        { id: 'patientInitials', label: 'Patient Initials' },
        { id: 'date', label: 'Date' },
        { id: 'discoveryPass', label: 'Discovery Pass' },
        { id: 'status', label: 'Status' },
        // { id: 'pdf', label: 'Prescription PDF' },
    ];

    const [prescriptionPage, setPrescriptionPage] = React.useState(0);
    const [prescriptionRowsPerPage, setPrescriptionRowsPerPage] = React.useState(5); 
    const [showPopup, setShowPopup] = React.useState(false);
    const [prescriptionDBdata, setPrescriptionDBdata] = React.useState([]);

    const handlePrescriptionPageChange = (event, newPage) => {
        setPrescriptionPage(newPage);
    };

    const handlePrescriptionRowsPerPageChange = (event) => {
        setPrescriptionRowsPerPage(+event.target.value);
        setPrescriptionPage(0); 
    };

    const handleAddPresClick = () => {
        setShowPopup(true);  // Open the popup
    };

    const handlePopupClose = () => {
        setShowPopup(false); // Close the popup
    };

    React.useEffect(() => {
        const handleGetPrescriptions = async () => {
            try {
                // TODO: call backend api here
                setPrescriptionDBdata(sampleData);
            } catch(error) {
                console.error('Error fetching prescription: ', error);
            }
        };

        handleGetPrescriptions();
    }, [])

    return (
        <div className='prescriber-prescriptions-component'>
            <div className='page-header'>
                <span>My Prescriptions</span>
            </div>
            <div className='content'>
                <div className='controls'>
                    <Button className='add-new-btn' onClick={handleAddPresClick}>Add New</Button>
                </div>
                <div className='table-container'>
                    <TableContainer className='table-cont'>
                        <Table className='table'>
                            <TableHead className='table-header'>
                                <TableRow className='header-row'>
                                    {prescriptionColumns.map((column) => (
                                        <TableCell key={column.id}>{column.label}</TableCell>
                                    ))}
                                    <TableCell key={"prescriptionButton"}><span>Prescription PDF</span></TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {prescriptionDBdata.slice(prescriptionPage * prescriptionRowsPerPage,
                                    prescriptionPage * prescriptionRowsPerPage + prescriptionRowsPerPage).map((row, id) => (
                                    <TableRow className='table-row' key={id}>
                                        {/* Render prescription columns */}
                                        {prescriptionColumns.map((column) => (
                                            <TableCell key={column.id}>{row[column.id]}</TableCell>
                                        ))}
                                        <TableCell key="prescriptionButton"> 
                                            {/* TODO: handle view prescriptions */}
                                            <Button className='btn' onClick={() => {}}>
                                                <span>View Prescription</span>
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                    <TablePagination
                        rowsPerPageOptions={[5, 10, 25]}
                        component="div"
                        count={prescriptionDBdata.length} 
                        rowsPerPage={prescriptionRowsPerPage}
                        page={prescriptionPage}
                        onPageChange={handlePrescriptionPageChange}
                        onRowsPerPageChange={handlePrescriptionRowsPerPageChange}
                    />
                </div>
            </div>
            <ReactPopup open={showPopup} closeOnDocumentClick={false} onClose={handlePopupClose}>
                <PatientAddPrescription onClose={handlePopupClose} /> 
            </ReactPopup>
        </div>
    );
};

export default PatientPrescriptions;
