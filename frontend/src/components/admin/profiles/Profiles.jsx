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

const Profiles = () => {
    const [prescriberPage, setPrescriberPage] = React.useState(0);
    const [prescriberRowsPerPage, setPrescriberRowsPerPage] = React.useState(5); 

    const [patientPage, setPatientPage] = React.useState(0);
    const [patientRowsPerPage, setPatientRowsPerPage] = React.useState(5);

    const [selectedTab, setSelectedTab] = React.useState(0); // State for selected tab

    // Separate Data for Prescribers and Patients
    const prescriberData = [ 
        { 
            id: 1,
            code: 'MD1001',
            first: 'John',
            last: 'Doe',
        },
    ];

    const patientData = [
        { 
            id: 1,
            code: 'PT3001', 
            first: 'Jane',
            last: 'Smith',
        },
    ];

    const columns = [ // Sample columns - add depending on what api returns
        { id: 'code', label: 'Code' },
        { id: 'first', label: 'First Name' },
        { id: 'last', label: 'Last Name' },
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
                    <Tab className={selectedTab === 1 ? 'active tab-label' : 'tab-label'} label="Patients" />
                </Tabs>
            </div>
            <div className='content'>
                <div className='table-container'>
                    <TableContainer className='table-cont'>
                        <Table className='table'>
                            <TableHead className='table-header'>
                                <TableRow className='header-row'>
                                    {columns.map((column) => (
                                        <TableCell key={column.id}>{column.label}</TableCell>
                                    ))}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {selectedTab === 0 ? (
                                    prescriberData.map((row) => (
                                        <TableRow className='table-row' key={row.id}>
                                            {/* Render prescriber columns */}
                                            {columns.map((column) => (
                                                <TableCell key={column.id}>{row[column.id]}</TableCell>
                                            ))}
                                        </TableRow>
                                    ))
                                ) : (
                                    patientData.map((row) => (
                                        <TableRow className='table-row' key={row.id}>
                                            {/* Render patient columns */}
                                            {columns.map((column) => (
                                                <TableCell key={column.id}>{row[column.id]}</TableCell>
                                            ))}
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
                            count={prescriberData.length} 
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
                            count={patientData.length} 
                            rowsPerPage={patientRowsPerPage}
                            page={patientPage}
                            onPageChange={handlePatientPageChange}
                            onRowsPerPageChange={handlePatientRowsPerPageChange}
                        />
                    )}
                </div>
            </div>
        </div>
    );
};

export default Profiles;
