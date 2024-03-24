import './Profiles.scss';
import { Button } from '@mui/material';
import * as React from 'react';
import TablePagination from '@mui/material/TablePagination';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab'; 
import decodeToken from '../../../token_handling/tokenHandling.js';
import { useNavigate } from 'react-router-dom';
import PrescriptionView from './PrescriptionView/PrescriptionView.jsx';
import ReactPopup from 'reactjs-popup';

const Profiles = () => {
    const [prescriberPage, setPrescriberPage] = React.useState(0);
    const [prescriberRowsPerPage, setPrescriberRowsPerPage] = React.useState(5); 
    const [prescriberDBdata, setPrescriberDBdata] = React.useState([]);
    const [patientDBdata, setPatientDBdata] = React.useState([]);
    const [isCoordinator, setIsCoordinator] = React.useState(true);

    const navigate = useNavigate();

    const [showPopup, setShowPopup] = React.useState(false);

    const handleButtonClick = () => {
        setShowPopup(true);  // Open the popup
    };

    const handlePopupClose = () => {
        setShowPopup(false); // Close the popup
    };

    React.useEffect(() => {
        const handleGetPrescribers = async () => {
            try {
                await fetch('https://notparx-prescriber-service.azurewebsites.net/api/getPrescriberProfiles/', {
                    method: 'GET',
                })
                .then (async response => {
                    if (response.ok) {
                        let data = await response.json();
                        console.log(data);
                        setPrescriberDBdata(data);
                    } else {
                        console.log('Error fetching prescribers: ', response.statusText);
                    }
                })
            } catch(error) {
                console.error('Error fetching prescriber: ', error);
            }
        };

        const handleGetPatients = async () => {
            try {
                await fetch('https://notparx-user-service.azurewebsites.net/api/getUserProfiles/', {
                    method: 'GET',
                })
                .then (async response => {
                    if (response.ok) {
                        let data = await response.json();
                        console.log(data);
                        setPatientDBdata(data);
                    } else {
                        console.log('Error fetching patients: ', response.statusText);
                    }
                })
            } catch(error) {
                console.error('Error fetching patients: ', error);
            }
        };

        const checkAdminType = () => {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/')
            }
            const decodedToken = decodeToken(token)
            if (decodedToken.user_type === 'Admin - Coordinator') {
                setIsCoordinator(true)
            } else {
                setIsCoordinator(false)
            }
        }

        checkAdminType()
        handleGetPrescribers();
        handleGetPatients();
    }, [])


    const [patientPage, setPatientPage] = React.useState(0);
    const [patientRowsPerPage, setPatientRowsPerPage] = React.useState(5);
    
    const [selectedTab, setSelectedTab] = React.useState(0); // State for selected tab


    const prescriberColumns = [ // Sample columns - add depending on what api returns
        { id: 'provDocID', label: 'Code' },
        { id: 'firstName', label: 'First Name' },
        { id: 'lastName', label: 'Last Name' },
        { id: 'email', label: 'Email' },
        { id: 'address', label: 'Address' },
        { id: 'city', label: 'City' },
        { id: 'province', label: 'Prov' },
        { id: 'college', label: 'Licensing College' },
        { id: 'licenseNum', label: 'License#' },
        // { id: '', label: 'Prescriptions'},
        // { id: "prescriptionButton", label: ''}
    ];

    const patientColumns = [
        { id: 'firstName', label: 'First Name' },
        { id: 'lastName', label: 'Last Name' },
        { id: 'email', label: 'Email' },
        { id: 'address', label: 'Address' },
        { id: 'city', label: 'City' },
        { id: 'province', label: 'Prov' },
        { id: 'language', label: 'Language' },
        { id: 'dpass', label: 'Discovery Pass'},
        { id: 'actionRequired', label: 'Action Required' }
    ];

    const handlePrescriberPageChange = (event, newPage) => {
        setPrescriberPage(newPage);
    };

    const handlePrescriberRowsPerPageChange = (event) => {
        setPrescriberRowsPerPage(+event.target.value);
        setPrescriberPage(0); 
    };

    const handlePatientPageChange = (event, newPage) => {
        setPatientPage(newPage);
    };

    const handlePatientRowsPerPageChange = (event) => {
        setPatientRowsPerPage(+event.target.value);
        setPatientPage(0); 
    };

    const handleTabChange = (event, newValue) => {
        setSelectedTab(newValue);
    };

    return (
        <div className='admin-profiles-component'>
            <div className='verif-header'>
                <Tabs value={selectedTab} onChange={handleTabChange}>
                    <Tab className={selectedTab === 0 ? 'active tab-label' : 'tab-label'} label="Prescribers" />
                    {isCoordinator && (
                        <Tab className={selectedTab === 1 ? 'active tab-label' : 'tab-label'} label="Patients" />
                    )}
                </Tabs>
            </div>
            <div className='content'>
                <div className='table-container'>
                    <TableContainer className='table-cont'>
                        <Table className='table'>
                            <TableHead className='table-header'>
                                {selectedTab === 0 ? (
                                    <TableRow className='header-row'>
                                    {prescriberColumns.map((column) => (
                                        <TableCell key={column.id}>{column.label}</TableCell>
                                    ))}

                                    <TableCell key = "prescriptionButton"> 
                                    </TableCell>

                                    </TableRow>
                                ) : (
                                    <TableRow className='header-row'>
                                    {patientColumns.map((column) => (
                                        <TableCell key={column.id}>{column.label}</TableCell>
                                    ))}

                                    <TableCell key = "prescriptionButton"> 
                                    </TableCell>

                                    </TableRow>
                                )}
                                
                            </TableHead>
                            <TableBody>
                                {selectedTab === 0 ? (
                                    prescriberDBdata.slice(prescriberPage * prescriberRowsPerPage,
                                        prescriberPage * prescriberRowsPerPage + prescriberRowsPerPage).map((row) => (
                                        <TableRow className='table-row' key={row.id}>
                                            {/* Render prescriber columns */}
                                            {prescriberColumns.map((column) => (
                                                <TableCell key={column.id}>{row[column.id]}</TableCell>
                                            ))}
                                            <TableCell key = "prescriptionButton"> 
                                                <Button className='upload-button' onClick={handleButtonClick}><span>View Prescriptions</span>
                                                </Button>
                                            </TableCell>
                                        </TableRow>
                                    ))
                                ) : (
                                    patientDBdata.slice(patientPage * prescriberRowsPerPage,
                                        patientPage * patientRowsPerPage + patientRowsPerPage).map((row) => (
                                        <TableRow className='table-row' key={row.id}>
                                            {/* Render patient columns */}
                                            {patientColumns.map((column) => (
                                                <TableCell key={column.id}>{row[column.id]}</TableCell>
                                            ))}

                                            <TableCell key = "prescriptionButton"> 
                                                <Button className='upload-button' onClick={handleButtonClick}><span>View Prescriptions</span>
                                                </Button>
                                            </TableCell>
                                        </TableRow>
                                    ))
                                )}
                            </TableBody>
                        </Table>
                    </TableContainer>
                    {selectedTab === 0 && ( // Show Prescriber Pagination
                        <TablePagination
                            rowsPerPageOptions={[5, 10, 25]}
                            component="div"
                            count={prescriberDBdata.length} 
                            rowsPerPage={prescriberRowsPerPage}
                            page={prescriberPage}
                            onPageChange={handlePrescriberPageChange}
                            onRowsPerPageChange={handlePrescriberRowsPerPageChange}
                        />
                    )}
                    {selectedTab === 1 && ( // Show Patient Pagination
                        <TablePagination
                            rowsPerPageOptions={[5, 10, 25]}
                            component="div"
                            count={patientDBdata.length} 
                            rowsPerPage={patientRowsPerPage}
                            page={patientPage}
                            onPageChange={handlePatientPageChange}
                            onRowsPerPageChange={handlePatientRowsPerPageChange}
                        />
                    )}
                </div>
            </div>
            <ReactPopup open={showPopup} closeOnDocumentClick={true} onClose={handlePopupClose}>
                <PrescriptionView onClose={handlePopupClose} /> 
            </ReactPopup>
        </div>
    );
};

export default Profiles;
