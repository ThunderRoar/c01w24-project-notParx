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

const Profiles = () => {

    const [rowsPerPage, setRowsPerPage] = React.useState(5); 
    const [page, setPage] = React.useState(0);

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0); // Reset page to 0 when rows per page change
    };

    const sampleData = [
        { 
            id: 1,
            code: 'MD1001',
            first: 'John',
            last: 'Doe',
            email: 'john.doe@example.com',
            street: '123 Main St',
            city: 'Toronto',
            province: 'ON',
            lang: 'EN',
            college: 'CPSO', 
            profession: 'Physician',
            licence: 'A12345',
            'view-prescription': true 
        },
        { 
            id: 2,
            code: 'RN2002',
            first: 'Jane',
            last: 'Smith',
            email: 'jane.smith@example.com',
            street: '456 Elm Ave',
            city: 'Ottawa',
            province: 'ON',
            lang: 'FR',
            college: 'CNO', 
            profession: 'Nurse',
            licence: 'B67890',
            'view-prescription': false
        },
        // Add more entries as needed... 
    ];
    
    const columns = [
        { id: 'code', label: 'Code' },
        { id: 'first', label: 'First Name' },
        { id: 'last', label: 'Last Name' },
        { id: 'email', label: 'Email' },
        { id: 'street', label: 'Street' },
        { id: 'city', label: 'City' },
        { id: 'province', label: 'Province' },
        { id: 'lang', label: 'Language' },
        { id: 'college', label: 'Licencing College' },
        { id: 'profession', label: 'Profession' },
        { id: 'licence', label: 'Licence No' },
        { id: 'view-prescription', label: '' },
    ];

    return (
        <div className='admin-verification-component'>
        <div className='verif-header'> Your CSVs </div>
        <div className='content'>
            <div className='controls'>
                <Button className='upload-button'>
                    <span>Upload CSV</span>
                </Button>
            </div>
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
                            {sampleData.map((row) => (
                                <TableRow className='table-row' key={row.id}>
                                    {columns.map((column) => (
                                        <TableCell key={column.id}>{row[column.id]}</TableCell>
                                    ))}
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
                <TablePagination
                    rowsPerPageOptions={[5, 10, 25]} // Options for rows per page
                    component="div"
                    count={sampleData.length} 
                    rowsPerPage={rowsPerPage}
                    page={page}
                    onPageChange={handleChangePage}
                    onRowsPerPageChange={handleChangeRowsPerPage}
                />
            </div>
        </div>
        </div>
    );
};

export default Profiles;