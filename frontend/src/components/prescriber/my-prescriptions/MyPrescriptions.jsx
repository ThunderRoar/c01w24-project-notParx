import './MyPrescriptions.scss';
import { Button } from '@mui/material';
import * as React from 'react';
import TablePagination from '@mui/material/TablePagination';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';

const MyPrescriptions = () => {
    const [prescriberPage, setPrescriberPage] = React.useState(0);
    const [prescriberRowsPerPage, setPrescriberRowsPerPage] = React.useState(5); 
    const [prescriberDBdata, setPrescriberDBdata] = React.useState([]);

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

        handleGetPrescribers();
    }, [])
    
    // const prescriberColumns = [ // Sample columns - add depending on what api returns
    //     { id: 'provDocID', label: 'Code' },
    //     { id: 'firstName', label: 'First Name' },
    //     { id: 'lastName', label: 'Last Name' },
    //     { id: 'email', label: 'Email' },
    //     { id: 'address', label: 'Address' },
    //     { id: 'city', label: 'City' },
    //     { id: 'province', label: 'Prov' },
    //     { id: 'college', label: 'Licensing College' },
    //     { id: 'licenseNum', label: 'License#' },
    //     // { id: '', label: 'Prescriptions'},
    //     // { id: "prescriptionButton", label: ''}
    // ];

    const prescriberColumns = [ // Sample columns - add depending on what api returns
        { id: 'provDocID', label: 'Provider Code' },
        { id: 'patientInitials', label: 'Patient Initials' },
        { id: 'date', label: 'Date' },
        { id: 'discoveryPass', label: 'Discovery Pass' },
        { id: 'patient', label: 'Matched Patient' },
        { id: 'status', label: 'Status' },
        { id: 'pdf', label: 'Prescription PDF' },
    ];

    const handlePrescriberPageChange = (event, newPage) => {
        setPrescriberPage(newPage);
    };

    const handlePrescriberRowsPerPageChange = (event) => {
        setPrescriberRowsPerPage(+event.target.value);
        setPrescriberPage(0); 
    };

    return (
        <div className='prescriber-prescriptions-component'>
            <div className='page-header'>
                <span>My Prescriptions</span>
                <Button className='btn' onClick={() => {}}>Add New</Button>
            </div>
            <div className='content'>
                <div className='table-container'>
                    <TableContainer className='table-cont'>
                        <Table className='table'>
                            <TableHead className='table-header'>
                                <TableRow className='header-row'>
                                {prescriberColumns.map((column) => (
                                    <TableCell key={column.id}>{column.label}</TableCell>
                                ))}

                                <TableCell key = "prescriptionButton"> 
                                </TableCell>

                                </TableRow>
                                
                            </TableHead>
                            <TableBody>
                                {prescriberDBdata.slice(prescriberPage * prescriberRowsPerPage,
                                    prescriberPage * prescriberRowsPerPage + prescriberRowsPerPage).map((row) => (
                                    <TableRow className='table-row' key={row.id}>
                                        {/* Render prescriber columns */}
                                        {prescriberColumns.map((column) => (
                                            <TableCell key={column.id}>{row[column.id]}</TableCell>
                                        ))}
                                        <TableCell key = "prescriptionButton"> 
                                            <Button className='btn' onClick={() => {}}><span>View Prescriptions</span>
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
                        count={prescriberDBdata.length} 
                        rowsPerPage={prescriberRowsPerPage}
                        page={prescriberPage}
                        onPageChange={handlePrescriberPageChange}
                        onRowsPerPageChange={handlePrescriberRowsPerPageChange}
                    />
                </div>
            </div>
        </div>
    );
};

export default MyPrescriptions;
