import React, { useState} from 'react';
import './PatientAddPrescription.scss';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import Checkbox from '@mui/material/Checkbox';
import { createTheme, ThemeProvider } from '@mui/material/styles'
import dayjs from 'dayjs';

const PatientAddPrescription = ({ onClose }) => {
    const today = dayjs(dayjs().format('YYYY-MM-DD'));

    const [date, setDate] = useState(today);
    const [provDocID, setProvDocID] = useState('');
    const [discoveryPass, setDiscoveryPass] = useState(false);
    const [invalidDate, setInvalidDate] = useState(null);
    const [invalidInput, setInvalidInput] = useState(false);
    const [error, setError] = useState(false);

    const handleCreate = async () => {
        if (!provDocID) {
            setInvalidInput(true);
            setError(true);
        } else if (false) {
            // TODO: check if provDocID exists in database
            setInvalidInput(true);
            setError(true);
        } else if (!error) {
            console.log(date.format('YYYY-MM-DD'));
            console.log(provDocID);
            console.log(discoveryPass);

            // Clear form inputs
            setDate(today);
            setProvDocID('');
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

    const handleProvDocIDChange = async (e) => {
        const inputValue = e.target.value.toUpperCase();
        setProvDocID(inputValue);
        setInvalidInput(false);
        setError(false || invalidDate);
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
                                    format="YYYY/MM/DD"
                                    onChange={handleDateChange}
                                    onError={(newError) => {setInvalidDate(newError); setError(newError);}}
                                />
                            </ThemeProvider>
                        </DemoContainer>
                    </LocalizationProvider>
                    { invalidDate && <span className='error-msg'>Invalid date</span> }
                </div>
                <div className='txt-field'>
                    <small>Unique Provider Code</small>
                    <input
                        type="text"
                        className="input-field"
                        placeholder="Unique Provider Code"
                        value={provDocID}
                        onChange={handleProvDocIDChange}
                    />
                    { invalidInput && <span className='error-msg'>Invalid provider code</span> }
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

export default PatientAddPrescription;
