import React, { useState} from 'react';
import './PrescriberAddPrescription.scss';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import Checkbox from '@mui/material/Checkbox';
import { createTheme, ThemeProvider } from '@mui/material/styles'
import dayjs from 'dayjs';
import decodeToken from '../../../../token_handling/tokenHandling.js';

const PrescriberAddPrescription = ({ onClose }) => {
    const today = dayjs(dayjs().format('YYYY-MM-DD'));

    const [date, setDate] = useState(today);
    const [patientInitials, setPatientInitials] = useState('');
    const [discoveryPass, setDiscoveryPass] = useState(false);
    const [invalidDate, setInvalidDate] = useState(null);
    const [invalidInput, setInvalidInput] = useState(false);
    const [error, setError] = useState(false);
    const [logError, setLogError] = useState(false);
    const [apiError, setApiError] = useState(false);

    const handleCreate = async () => {
        if (!patientInitials || patientInitials.length < 2) {
            setInvalidInput(true);
            setError(true);
        }
        else if (!error) {
            console.log(date.format('YYYY-MM-DD'));
            console.log(patientInitials);
            console.log(discoveryPass);

            //Log prescription
            const token = localStorage.getItem('token');
            if (token) {
                const decodedToken = decodeToken(token)
                if (!decodedToken) {
                    setApiError(true)
                } else {
                    const prescriberID = decodedToken.username
                    const initials = patientInitials
                    const formattedDate = date.format('YYYY/MM/DD')
                    try {
                        const response = await fetch('https://notparx-prescription-service.azurewebsites.net/api/logPrescriberPrescription/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ "date": formattedDate, discoveryPass, prescriberID, initials })
                            });
                            const responseData = await response.json();
            
                            if (response.ok) {
                                console.log("Prescription Log Success")

                                // Clear form inputs
                                setDate(today);
                                setPatientInitials('');
                                setDiscoveryPass(false);

                                // Clear errors
                                setError(false);
                                setInvalidDate(null);
                                setInvalidInput(false);
                                setApiError(false);
                                setLogError(false);

                                // Close Popup
                                onClose();
                            } else {
                                setLogError(true)
                                console.error("Prescription Log Fail");
                            }
                    } catch (error) {
                        setApiError(true)
                        console.error("Error");
                    }
                }
            } else {
                setApiError(true)
            }
        }
    }

    const handleDateChange = async (newDate) => {
        setDate(newDate);
    }

    const handlePatientInitialsChange = async (e) => {
        const inputValue = e.target.value.toUpperCase().replace(/[^A-Z]/g, '');
        setPatientInitials(inputValue);
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
            {logError && <span className='duplicate-log-error'>Prescription already logged</span>}
            {apiError && <span className='api-log-error'>Error logging prescription. Ensure information is correct and try again</span>}
            <div className="form-content">
                <div className='txt-field'>
                    <small>Date</small>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DemoContainer components={['DatePicker']}>
                            <ThemeProvider theme={customDatePicker}>
                                <DatePicker
                                    slotProps={{ textField: { size: 'small' } }}
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
                    <small>Patient Initials (FirstLast)</small>
                    <input
                        type="text"
                        className="input-field"
                        placeholder="Patient Initials"
                        value={patientInitials}
                        maxLength={2}
                        onChange={handlePatientInitialsChange}
                    />
                    { invalidInput && <span className='error-msg'>Invalid input</span> }
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

export default PrescriberAddPrescription;
