import './PrescriptionView.scss';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import { TableContainer, Table, TableHead, TableBody, TableRow, TableCell } from '@mui/material';
import React from 'react';
import { Button } from '@mui/material';
import TablePagination from '@mui/material/TablePagination';

const PrescriptionView = ( { onClose, userId, type } ) => {

    const [prescriptionDBdata, setPrescriptionDBdata] = React.useState([]);
    const [prescriberPage, setPrescriberPage] = React.useState(0);
    const [prescriberRowsPerPage, setPrescriberRowsPerPage] = React.useState(5);
    const [patientPage, setPatientPage] = React.useState(0);
    const [patientRowsPerPage, setPatientRowsPerPage] = React.useState(5);

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

    React.useEffect(() => {
        const handleGetPrescriberPrescriptions = async () => {
            try {
                const response = await fetch(`https://notparx-prescription-service.azurewebsites.net/api/prescriberPrescriptions/${userId}/`, {
                    method: 'GET',
                });
    
                if (response.ok) {
                    let data = await response.json();
                    for (let p of data) {
                        p["patientInitials"] = p["prescriptionID"].slice(-2);
                        p["discoveryPassPrescribed"] = p["discoveryPassPrescribed"].toString();
                    }
                    setPrescriptionDBdata(data);
                } else {
                    console.error('Error fetching prescriptions: ', response.statusText);
                }
            } catch(error) {
                console.error('Error fetching prescriptions for prescriber: ', error);
            }
        };

        const handleGetPatientPrescriptions = async () => {
            try {
                await fetch('https://notparx-prescription-service.azurewebsites.net/api/patientPrescriptions/' + userId + '/', {
                    method: 'GET',
                })
                .then (async response => {
                    if (response.ok) {
                        let data = await response.json();
                        console.log(data);
                        for (let p of data) {
                            p["patientInitials"] = p["prescriptionID"].slice(-2);
                            p["discoveryPassPrescribed"] = p["discoveryPassPrescribed"].toString();
                        }
                        setPrescriptionDBdata(data);
                    } else {
                        console.error('Error fetching prescriptions: ', response.statusText);
                    }
                })
            } catch(error) {
                console.error('Error fetching prescriptions: ', error);
            }
        };
    
        (type === 'prescriber') ? handleGetPrescriberPrescriptions() : handleGetPatientPrescriptions();
    }, [userId])

    const prescriptionColumnsPrescriber = [ // Sample columns - add depending on what api returns
        { id: 'prescriberCode', label: 'Provider Code' },
        { id: 'patientInitials', label: 'Patient Initials' },
        { id: 'dateOfPrescription', label: 'Date' },
        { id: 'discoveryPassPrescribed', label: 'Discovery Pass' },
        { id: 'matchedPatient', label: 'Matched Patient' },
        { id: 'prescriberStatus', label: 'Status' },
        // { id: 'pdf', label: 'Prescription PDF' },
    ];

    const prescriptionColumnsPatient = [
        { id: 'prescriberCode', label: 'Provider Code' },
        { id: 'patientInitials', label: 'Patient Initials' },
        { id: 'dateOfPrescription', label: 'Date' },
        { id: 'discoveryPassPrescribed', label: 'Discovery Pass' },
        { id: 'patientStatus', label: 'Status' },
        // { id: 'pdf', label: 'Prescription PDF' },
    ];

    const handleDownloadPrescription = async (prescriptionID) => {
        console.log(prescriptionID);
        let url = `https://notparx-prescription-service.azurewebsites.net/api/downloadprescription/${prescriptionID}/`;
        
        try {
            const response = await fetch(url, {
                method: 'GET',
                // Add headers if needed, e.g., Authorization for protected routes
            });        
            if (!response.ok) {
                console.error('Error downloading prescription: ', response.statusText);
            }
            let contentDisposition = response.headers.get('Content-Disposition');
            let filename = "prescription.pdf"; // Default filename if not found
            console.log(contentDisposition);
            if (contentDisposition) {
                let matches = contentDisposition.match(/filename="?(.+)"?/);
                if (matches.length > 1) {
                    filename = matches[1];
                }
                filename=filename.substring(0, filename.length-1);
            }            

            // Process the response as a Blob to handle the binary PDF data
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.setAttribute('download', filename); // Set the file name for the download
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        }
        catch (error) {
            console.error('Download error:', error);
            // Handle error scenario, e.g., show a notification or message to the user
        }
    }

    return (
        <div className="prescription-view">
            <div className="popup-header">
                <div>Patient's Prescriptions</div>
                <HighlightOffIcon onClick={onClose} className='close-icon' />
            </div>
            <div className='content'>
                <div className='table-container'>
                    <TableContainer className='table-cont'>
                        <Table className='table'>
                            <TableHead className='table-header'>
                                {type === 'prescriber' ? (
                                    <TableRow className='header-row'>
                                    {prescriptionColumnsPrescriber.map((column) => (
                                        <TableCell key={column.id}>{column.label}</TableCell>
                                    ))}

                                    <TableCell key = "prescriptionButton"> 
                                    </TableCell>

                                    </TableRow>
                                ) : (
                                    <TableRow className='header-row'>
                                    {prescriptionColumnsPatient.map((column) => (
                                        <TableCell key={column.id}>{column.label}</TableCell>
                                    ))}

                                    <TableCell key = "prescriptionButton"> 
                                    </TableCell>

                                    </TableRow>
                                )}
                            </TableHead>
                            <TableBody>
                                {type === 'prescriber' ? (
                                    prescriptionDBdata.slice(prescriberPage * prescriberRowsPerPage,
                                        prescriberPage * prescriberRowsPerPage + prescriberRowsPerPage).map((row) => (
                                        <TableRow className='table-row' key={row.id}>
                                            {/* Render prescriber columns */}
                                            {prescriptionColumnsPrescriber.map((column) => (
                                                <TableCell key={column.id}>{row[column.id]}</TableCell>
                                            ))}
                                            <TableCell key = "prescriptionButton"> 
                                                <Button 
                                                    className='upload-button'
                                                    onClick={() => handleDownloadPrescription(row["prescriptionID"])}
                                                >
                                                    <span>Download Prescription</span>
                                                </Button>
                                            </TableCell>
                                        </TableRow>
                                    ))
                                ) : (
                                    prescriptionDBdata.slice(patientPage * prescriberRowsPerPage,
                                        patientPage * patientRowsPerPage + patientRowsPerPage).map((row) => (
                                        <TableRow className='table-row' key={row.id}>
                                            {/* Render patient columns */}
                                            {prescriptionColumnsPatient.map((column) => (
                                                <TableCell key={column.id}>{row[column.id]}</TableCell>
                                            ))}

                                            <TableCell key = "prescriptionButton"> 
                                                <Button 
                                                    className='upload-button'
                                                    onClick={() => handleDownloadPrescription(row["prescriptionID"])}
                                                >
                                                    <span>Download Prescription</span>
                                                </Button>
                                            </TableCell>
                                        </TableRow>
                                    ))
                                )}
                            </TableBody>
                        </Table>
                    </TableContainer>
                    {type === 'prescriber' && (
                        <TablePagination
                            rowsPerPageOptions={[5, 10, 25]}
                            component="div"
                            count={prescriptionDBdata.length} 
                            rowsPerPage={prescriberRowsPerPage}
                            page={prescriberPage}
                            onPageChange={handlePrescriberPageChange}
                            onRowsPerPageChange={handlePrescriberRowsPerPageChange}
                        />
                    )}
                    {type === 'patient' && (
                        <TablePagination
                            rowsPerPageOptions={[5, 10, 25]}
                            component="div"
                            count={prescriptionDBdata.length} 
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

export default PrescriptionView;