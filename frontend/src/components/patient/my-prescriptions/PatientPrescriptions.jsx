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
import decodeToken from '../../../token_handling/tokenHandling.js';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';

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
    const [actionRequired, setActionRequired] =  React.useState(false);
    const [showUpdateAddress, setShowUpdateAddress] = React.useState(false);
    const [invalidInput, setInvalidInput] = React.useState(false);
    const [address, setAddress] = React.useState('');

    const handleActionRequired = async () => {
        const token = localStorage.getItem('token');
        if (token) {
            const decodedToken = decodeToken(token)
            if (!decodedToken) {
                console.error("Error with token")
            } else {
                const username = decodedToken.username
                try {
                    const response = await fetch('https://notparx-user-service.azurewebsites.net/api/getActionRequired/' + username + '/', {
                        method: 'GET'
                        });
                        const responseData = await response.json();
        
                        if (response.ok) {
                            console.log("Successfully got actionRequired")
                            setActionRequired(responseData["actionRequired"])

                        } else {
                            console.log("hello")
                            console.error("Error with username in retrieving actionRequired");
                        }
                } catch (error) {
                    console.log("hello2")
                    console.error("Error retrieving actionRequired");
                }
            }
        }
    }

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

    const handleAddAddressClick = () => {
        setShowUpdateAddress(true);
    };

    const handlePopupClose = () => {
        setShowPopup(false); // Close the popup
        setShowUpdateAddress(false);
        setInvalidInput(false)
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
        handleActionRequired();
    }, [])

    const handleAddressChange = async (e) => {
        const inputValue = e.target.value;
        setAddress(inputValue);
        setInvalidInput(false);
    }

    const handleAddAddress = async () => {
        if (!address) {
            setInvalidInput(true);
            return
        }
        const token = localStorage.getItem('token');
        if (token) {
            const decodedToken = decodeToken(token)
            if (!decodedToken) {
            } else {
                const username = decodedToken.username
                try {
                    const response = await fetch('https://notparx-user-service.azurewebsites.net/api/updateUserAddress/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ username, address })
                        });
        
                        if (response.ok) {
                            console.log("Successfully updated address");
                            setActionRequired(false)
                            setShowUpdateAddress(false);

                        } else {
                            console.error("Error updating address");
                        }
                } catch (error) {
                    console.error("Error. Ensure address is correct");
                }
            }
        }
    }

    return (
        <div className='prescriber-prescriptions-component'>
            <div className='page-header'>
                <span>My Prescriptions</span>
            </div>
            <div className='content'>
                    {actionRequired && (
                        <div className='button-section'>
                            <div className='action-required'>
                                <h>ACTION REQUIRED! PLEASE ADD ADDRESS!</h>
                                <Button className='action-required-button' onClick={handleAddAddressClick}>Add Address</Button>
                            </div>
                            <Button className='add-new-btn' onClick={handleAddPresClick}>Add New</Button>
                        </div>
                    )}
                    {!actionRequired && (
                        <div className='controls'>
                            <Button className='add-new-btn' onClick={handleAddPresClick}>Add New</Button>
                        </div>
                    )}
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
            <ReactPopup open={showUpdateAddress} closeOnDocumentClick={false}>
                <div className='content-popup'>
                    <div className="header">
                        <div>Update Address</div>
                        <HighlightOffIcon onClick={handlePopupClose} className='close-icon' />
                    </div>
                    <div className="form-content">
                        <div className='txt-field'>
                            <small>Address</small>
                            <input
                                type="text"
                                className="input-field"
                                placeholder="Address"
                                value={address}
                                onChange={handleAddressChange}
                            />
                            { invalidInput && <span className='error-msg'>Invalid address</span> }
                        </div>
                        <button className="btn" onClick={handleAddAddress}>Update Address</button>
                    </div>
                </div>
            </ReactPopup>
        </div>
    );
};

export default PatientPrescriptions;
