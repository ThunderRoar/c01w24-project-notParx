import React, { useState} from 'react';
import './AddNewPrescription.scss';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import Checkbox from '@mui/material/Checkbox';
import { createTheme, ThemeProvider } from '@mui/material/styles'
import dayjs from 'dayjs';

const AddNewPrescription = ({ onClose }) => {
    const today = dayjs(dayjs().format('YYYY-MM-DD'));

    const [date, setDate] = useState(today);
    const [patientInitials, setPatientInitials] = useState('');
    const [discoveryPass, setDiscoveryPass] = useState(false);
    const [invalidDate, setInvalidDate] = useState(null);
    const [invalidInput, setInvalidInput] = useState(false);
    const [error, setError] = useState(false);

    const handleCreate = async () => {
        if (!patientInitials) {
            setInvalidInput(true);
            setError(true);
        }
        else if (!error) {
            console.log(date.format('YYYY-MM-DD'));
            console.log(patientInitials);
            console.log(discoveryPass);

            // Clear form inputs
            setDate(today);
            setPatientInitials('');
            setDiscoveryPass(false);

            // Clear errors
            setError(false);
            setInvalidDate(null);
            setInvalidInput(false);

            // Close Popup
            onClose();
        }
    }

    const handleDateChange = async (newDate) => {
        setDate(newDate);
    }

    const handlePatientInitialsChange = async (e) => {
        const inputValue = e.target.value.toUpperCase().replace(/[^A-Z]/g, '');
        setPatientInitials(inputValue);
        setInvalidInput(false);
    }

    const handleCheck = async (e) => {
        setDiscoveryPass(e.target.checked);
    }

    const customDatePicker = createTheme({
        components: {
            MuiTextField: {
                defaultProps: {
                    className: 'custom-textfield custom-style',
                },
            },
        }
    })

    return (
        <div className="add-content">
            <div className="popup-header">
                <div>Add a New Prescription</div>
                <HighlightOffIcon onClick={onClose} className='close-icon' />
            </div>
            <div className="form-content">
                <div className='txt-field'>
                    <small>Date</small>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DemoContainer components={['DatePicker']}>
                            <ThemeProvider theme={customDatePicker}>
                                <DatePicker
                                    slotProps={{ textField: { size: 'small' } }}
                                    minDate={today}
                                    value={date}
                                    onChange={handleDateChange}
                                    onError={(newError) => {setInvalidDate(newError); setError(newError);}}
                                />
                            </ThemeProvider>
                        </DemoContainer>
                    </LocalizationProvider>
                    { invalidDate && <text>Invalid date</text> }
                </div>
                <div className='txt-field'>
                    <small>Patient Initials (FirstLast)</small>
                    <input
                        type="text"
                        className="input-field"
                        placeholder="Patient Initials"
                        value={patientInitials}
                        maxLength={2}
                        onChange={handlePatientInitialsChange}
                    />
                    { invalidInput && <text>Invalid input</text> }
                </div>
                <div className='checkbox-field'>
                    <small>PC Discovery Pass</small>
                    <Checkbox
                        inputProps={{ 'aria-label': 'Checkbox' }}
                        color="success"
                        checked={discoveryPass}
                        onChange={handleCheck}
                    />
                </div>
            </div>
            <button className="btn" onClick={handleCreate}>Create a Prescription</button>
        </div>
    );
};

export default AddNewPrescription;
