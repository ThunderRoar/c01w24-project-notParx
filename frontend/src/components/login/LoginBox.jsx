import './LoginBox.scss';
import * as React from 'react';
import loginImage from '../../resources/img/LoginText.png';
import { useNavigate } from 'react-router-dom';
import "@fontsource/ubuntu";
import "@fontsource/ubuntu/400.css";
import "@fontsource/ubuntu/400-italic.css";
import { FaRegCircle, FaCircle } from "react-icons/fa";
import { IoEyeOutline } from "react-icons/io5";
import { FiLoader } from "react-icons/fi";

const LoginBox = () => {

    const [activeButton, setActiveButton] = React.useState('Patient');
    const [currentView, setCurrentView] = React.useState('login');
    const [username, setUsername] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [firstName, setFirstName] = React.useState('');
    const [lastName, setLastName] = React.useState('');
    const [email, setEmail] = React.useState('');
    const [language, setLanguage] = React.useState('');
    const [city, setCity] = React.useState('');
    const [address, setAddress] = React.useState("");
    const [provDocID, setProvDocID] = React.useState('');
    const [province, setProvince] = React.useState('AB');
    const [boxHeight, setBoxHeight] = React.useState(400);
    const [boxWidth, setBoxWidth] = React.useState(350);
    const [showPassword, setShowPassword] = React.useState(false)
    const [loginError, setLoginError] = React.useState(false)
    const [apiError, setApiError] = React.useState(false)
    const [emailError, setEmailError] = React.useState(false)
    const [usernameExistsError, setUsernameExistsError] = React.useState(false)
    const [invalidFieldsError, setInvalidFieldsError] = React.useState(false)
    const [prescriberAlreadySignedUp, setPrescriberAlreadySignedUp] = React.useState(false)
    const [loading, setLoading] = React.useState(false)

    const emailRegex = /^[\w.!#$%&*+-/=?^_{|}~]+@[a-zA-Z0-9-]+\.[A-z]+$/;
    const login = 'login'
    const signUp = 'signUp'
    const prescriber = 'Prescriber'
    const patient = 'Patient'
    const admin = 'Admin'
    const loginText = loginImage
    const navigate = useNavigate()

    const typeSwitchClicked = (buttonId) => {
        removeErrors()
        if (currentView === signUp) {
            if (buttonId === prescriber) {
                setBoxHeight(650)
            } else {
                setBoxHeight(710)
            }
        }
        setActiveButton(buttonId);
    };

    const switchViewClicked = (buttonID) => {
        removeErrors()
        if (activeButton === admin) {
            setActiveButton(patient)
        }

        if (buttonID === 'login') { // Sign up view
            if (activeButton === prescriber) {
                setBoxHeight(650)
            } else {
                setBoxHeight(710)
            }
            setBoxWidth(350)
            setCurrentView('signUp')
        } else { // Login View
            setBoxHeight(400)
            setBoxWidth(350)
            setCurrentView('login')
        }
    }

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    }

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    }

    const handleFirstNameChange = (event) => {
        setFirstName(event.target.value);
    }

    const handleLastNameChange = (event) => {
        setLastName(event.target.value);
    }

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    }

    const handleLanguageChange = (event) => {
        setLanguage(event.target.value);
    }

    const handleAddressChange = (event) => {
        setAddress(event.target.value);
    }

    const handleCityChange = (event) => {
        setCity(event.target.value);
    }

    const handleProvDocIDChange = (event) => {
        setProvDocID(event.target.value);
    }

    const handleProvinceChange = (event) => {
        setProvince(event.target.value)
    }

    const toggleShowPassword = () => {
        setShowPassword(!showPassword)
    }

    const removeErrors = () => {
        setLoginError(false)
        setApiError(false)
        setEmailError(false)
        setUsernameExistsError(false)
        setInvalidFieldsError(false)
        setPrescriberAlreadySignedUp(false)
    }

    const checkValidEmail = () => {
        if (!emailRegex.test(email)) {
            setEmailError(true)
            return false
        }
        return true
    }

    const loginClicked = async () => {
        removeErrors()
        setLoading(true)

        try {
            if (activeButton === patient) {
                const response = await fetch('https://notparx-user-service.azurewebsites.net/api/loginUser/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
                });
                const responseData = await response.json();
                if (response.ok) {
                    console.log("Login Success")
                    localStorage.setItem('token', responseData.token)
                    navigate('/Patient')
                } else {
                    setLoginError(true)
                    console.error(response.error);
                }
            } else if (activeButton === prescriber) {
                const response = await fetch('https://notparx-user-service.azurewebsites.net/api/loginPrescriber/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
                });
                const responseData = await response.json();

                if (response.ok) {
                    console.log("Login Success")
                    localStorage.setItem('token', responseData.token)
                    navigate('/Prescriber')
                } else {
                    setLoginError(true)
                    console.error("Login Fail");
                }
            } else {
                const response = await fetch('https://notparx-user-service.azurewebsites.net/api/loginAdmin/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
                });
                const responseData = await response.json();

                if (response.ok) {
                    console.log("Login Success")
                    localStorage.setItem('token', responseData.token)
                    navigate('/Admin')
                } else {
                    setLoginError(true)
                    console.error("Login Fail");
                }
            }
        } catch (error) {
                setApiError(true)
                console.error("Login Error");
        } finally {
            setLoading(false)
        }
    }

    const signUpClicked = async () => {
        removeErrors()
        setLoading(true)
        try {
            if (!checkValidEmail()) {
                return
            }

            if (activeButton === patient) {
                const bodyAddress = address === "" ? "DNE" : address;
                const response = await fetch('https://notparx-user-service.azurewebsites.net/api/registerUser/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password, firstName, lastName, "address" : bodyAddress, city, province, language, email })
                });
                const responseData = await response.json();

                if (response.ok) {
                    console.log("Patient Register Success")
                    localStorage.setItem('token', responseData.token)
                    navigate('/Patient')
                } else if (responseData.error === "Username has already been used"){
                    setUsernameExistsError(true)
                    console.error("Patient Register Fail");
                } else {
                    setInvalidFieldsError(true)
                    console.error("Patient Register Error")
                    console.log(response.error)
                }
            } else {
                const response = await fetch('https://notparx-user-service.azurewebsites.net/api/registerPrescriber/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ provDocID, password, address, city, language, email })
                });
                const responseData = await response.json();

                if (response.ok) {
                    console.log("Prescriber Register Success")
                    localStorage.setItem('token', responseData.token)
                    navigate('/Prescriber')
                } else if (responseData.error === "Already signed up"){
                    setPrescriberAlreadySignedUp(true)
                    console.error("Presciber Register Fail");
                } else {
                    setInvalidFieldsError(true)
                    console.log("Presciber Register Fail")
                }
            }
        } catch (error) {
                setInvalidFieldsError(true)
                console.error("Register Error");
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className='screen-container'>
            {loginError && (
                <div className='login-error-popup'>
                    Invalid username or password. Please try again.
                </div>
            )}
            {apiError && (
                <div className='login-error-popup'>
                    Something went wrong. Please try again.
                </div>
            )}
            {emailError && (
                <div className='signup-error-popup'>
                    Please enter a valid email.
                </div>
            )}
            {usernameExistsError && (
                <div className='signup-error-popup'>
                    Username already exists. Please enter a new username.
                </div>
            )}
            {invalidFieldsError && (
                <div className='signup-error-popup'>
                    Please ensure all fields have been filled out and are correct, then try again.
                </div>
            )}
            {prescriberAlreadySignedUp && (
                <div className='signup-error-popup'>
                    Account already exists with this PaRx ID.
                </div>
            )}
            <div className='image-container'>
                <img src={loginText} alt=''/>
            </div>
            <div className='login-component'>
                    <div className='content'>
                        <div className='table-container' style={{height: `${boxHeight}px`, width: `${boxWidth}px`}}>
                            {currentView === login && (<h2>Log in</h2>)}
                            {currentView === signUp && (<h2>Sign Up</h2>)}
                            <p>Who are you?</p>
                            <div className='button-group'>
                                <button
                                    className={`type-button ${activeButton === patient ? 'active' : ''}`}
                                    onClick={() => typeSwitchClicked(patient)} >
                                        <div className='row'>
                                            {activeButton === patient && (<FaRegCircle strokeWidth={35} size={15} color="white" />)}
                                            {activeButton !== patient && (<FaCircle size={15} color="#E3EAE1" />)}
                                            <text style={{marginLeft: `5px`}}>Patient</text>
                                        </div>
                                </button>
                                <button
                                    className={`type-button ${activeButton === prescriber ? 'active' : ''}`}
                                    onClick={() => typeSwitchClicked(prescriber)} >
                                    <div className='row'>
                                            {activeButton === prescriber && (<FaRegCircle strokeWidth={35} size={15} color="white" />)}
                                            {activeButton !== prescriber && (<FaCircle size={15} color="#E3EAE1" />)}
                                            <text style={{marginLeft: `5px`}}>Prescriber</text>
                                        </div>
                                </button>
                                {currentView === login && (
                                    <button
                                        className={`type-button ${activeButton === admin ? 'active' : ''}`}
                                        onClick={() => typeSwitchClicked(admin)} >
                                        <div className='row'>
                                            {activeButton === admin && (<FaRegCircle strokeWidth={35} size={15} color="white" />)}
                                            {activeButton !== admin && (<FaCircle size={15} color="#E3EAE1" />)}
                                            <text style={{marginLeft: `5px`}}>Admin</text>
                                        </div>
                                    </button>
                                )}
                            </div>
                            {currentView === signUp && (
                                <>
                                {activeButton === prescriber && (
                                    <>
                                    <small>Unique PaRx ID</small>
                                    <input type="text" className="input-field" placeholder="Unique PaRx ID" value={provDocID} onChange={handleProvDocIDChange}/>
                                    </>
                                )}

                                {activeButton === patient && (
                                    <div className='row-input'>
                                        <div className='column' style={{marginRight: `12px`}}>
                                            <small>First Name</small>
                                            <input type="text" className="input-field" placeholder="First Name" value={firstName} onChange={handleFirstNameChange}/>
                                        </div>
                                        <div className='column'>
                                            <small>Last Name</small>
                                            <input type="text" className="input-field" placeholder="Last Name" value={lastName} onChange={handleLastNameChange}/>
                                        </div>
                                    </div>
                                )}
                                <small>Email</small>
                                <input type="text" className="input-field" placeholder="Email" value={email} onChange={handleEmailChange}/>
                                <small>Language</small>
                                <input type="text" className="input-field" placeholder="Language" value={language} onChange={handleLanguageChange}/>
                                {activeButton === patient && (
                                    <div className='row-input'>
                                        <div className='column'>
                                            <small>Province</small>
                                            <div style={{marginTop: `12px`, marginRight: `50px`}}>
                                                <select value={province} onChange={handleProvinceChange}>
                                                    <option value='AB'>AB</option>
                                                    <option value='BC'>BC</option>
                                                    <option value='ON'>ON</option>
                                                    <option value='MB'>MB</option>
                                                    <option value='NB'>NB</option>
                                                    <option value='NL'>NL</option>
                                                    <option value='NS'>NS</option>
                                                    <option value='PE'>PE</option>
                                                    <option value='QC'>QC</option>
                                                    <option value='SK'>SK</option>
                                                </select>
                                            </div>
                                        </div>
                                        <div className='column2'>
                                            <small>City</small>
                                            <input type="text" className="input-field" placeholder="City" value={city} onChange={handleCityChange}/>
                                        </div>
                                    </div>
                                )}
                                {activeButton === prescriber && (
                                    <>
                                    <small>City</small>
                                    <input type="text" className="input-field" placeholder="City" value={city} onChange={handleCityChange}/>
                                    </>
                                )}
                                <small>Address</small>
                                <input type="text" className="input-field" placeholder="Address (Optional)" value={address} onChange={handleAddressChange}/>
                                </>
                            )}
                            {(currentView === login || (currentView === signUp && activeButton === patient)) && (
                                <>
                                <small>Username</small>
                                <input type="text" className="input-field" placeholder="Username" value={username} onChange={handleUsernameChange}/>
                                </>
                            )}
                            <small>Password</small>
                            <div className='password-input-container'>
                                <input type={showPassword ? 'text' : 'password'} className='input-field' placeholder="Password" value={password} onChange={handlePasswordChange}/>
                                <button className='password-toggle-button' onClick={toggleShowPassword}>
                                    <IoEyeOutline/>
                                </button>
                            </div>
                            
                            {loading && (
                                <div className='get-started-button'>
                                    <center>
                                        <FiLoader></FiLoader>
                                    </center>
                                </div>
                            )}
                            {!loading && currentView === signUp && (
                                <button className='get-started-button' onClick={() => signUpClicked()}>
                                    <span>Get Started</span>
                                </button>
                            )}
                            {!loading && currentView === login && (
                                <button className='get-started-button' onClick={() => loginClicked()}>
                                    <span>Get Started</span>
                                </button>
                            )}
                            <div className='row'>
                            {currentView === login && (
                                <button className='switch-screen-button' onClick={() => switchViewClicked(login)}>
                                    <span>Create a new account</span>
                                </button>)}
                            {currentView === signUp && (
                                <button className='switch-screen-button' onClick={() => switchViewClicked(signUp)}>
                                    <span>Use an existing account</span>
                                </button>)}
                            </div> 
                        </div>
                    </div>
            </div>
        </div>
        
    );
};

export default LoginBox;