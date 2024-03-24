import './PrescriptionView.scss';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import { TableContainer, Table, TableHead, TableBody, TableRow, TableCell } from '@mui/material';

const PrescriptionView = ( { onClose } ) => {

    const prescriptionData = [
        { name: 'Medication 1', strength: '500mg', frequency: 'Twice daily' },
        { name: 'Medication 2', strength: '25mg', frequency: 'Once daily' },
    ];

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
                                <TableRow className='header-row'>
                                    <TableCell>Name</TableCell>
                                    <TableCell>Strength</TableCell>
                                    <TableCell>Frequency</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {prescriptionData.map((row) => (
                                    <TableRow key={row.name} className='table-row'>
                                        <TableCell>{row.name}</TableCell>
                                        <TableCell>{row.strength}</TableCell>
                                        <TableCell>{row.frequency}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </div>
            </div>
        </div>
    );

};

export default PrescriptionView;