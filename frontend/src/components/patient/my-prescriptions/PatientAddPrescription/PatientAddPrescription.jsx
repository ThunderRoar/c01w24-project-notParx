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
import decodeToken from '../../../../token_handling/tokenHandling.js';

const PatientAddPrescription = ({ onClose }) => {
    const today = dayjs(dayjs().format('YYYY-MM-DD'));

    const [date, setDate] = useState(today);
    const [provDocID, setProvDocID] = useState('');
    const [discoveryPass, setDiscoveryPass] = useState(false);
    const [invalidDate, setInvalidDate] = useState(null);
    const [invalidInput, setInvalidInput] = useState(false);
    const [error, setError] = useState(false);
    const [logError, setLogError] = useState(false);
    const [apiError, setApiError] = useState(false);
    const [noPrescriberError, setNoPrescriberError] = useState(false);

    const handleCreate = async () => {
        if (!provDocID) {
            setInvalidInput(true);
            setError(true);
        } else if (!error) {
            console.log(date.format('YYYY-MM-DD'));
            console.log(provDocID);
            console.log(discoveryPass);

            //Log prescription
            const token = localStorage.getItem('token');
            if (token) {
                const decodedToken = decodeToken(token)
                if (!decodedToken) {
                    setApiError(true)
                } else {
                    const username = decodedToken.username
                    const prescriberID = provDocID
                    const formattedDate = date.format('YYYY-MM-DD')
                    try {
                        const response = await fetch('https://notparx-prescription-service.azurewebsites.net/api/logUserPrescription/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ username, "date": formattedDate, discoveryPass, prescriberID })
                            });
                            const responseData = await response.json();
            
                            if (response.ok) {
                                console.log("Prescription Log Success")

                                // Clear form inputs
                                setDate(today);
                                setProvDocID('');
                                setDiscoveryPass(false);

                                // Clear errors
                                setError(false);
                                setInvalidDate(null);
                                setInvalidInput(false);
                                setApiError(false);
                                setLogError(false);
                                setNoPrescriberError(false);

                                // Close Popup
                                onClose();
                            } else {
                                if (responseData.error === "No prescriber with that ID") {
                                    setNoPrescriberError(true)
                                    console.error("Invalid prescriberID");
                                } else {
                                    setLogError(true)
                                    console.error("Prescription Log Fail");
                                }
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
        setApiError(false);
        setLogError(false);
    }

    const handleProvDocIDChange = async (e) => {
        const inputValue = e.target.value.toUpperCase();
        setProvDocID(inputValue);
        setInvalidInput(false);
        setApiError(false);
        setLogError(false);
        setNoPrescriberError(false);
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
            {noPrescriberError && <span className='duplicate-log-error'>No prescriber with that ID</span>}
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
