import './LoginBox.scss';
import * as React from 'react';
import loginImage from '../../resources/img/LoginText.png';
import { useNavigate } from 'react-router-dom';
import "@fontsource/ubuntu";
import "@fontsource/ubuntu/400.css";
import "@fontsource/ubuntu/400-italic.css";
import { FaRegCircle, FaCircle } from "react-icons/fa";
import { IoEyeOutline } from "react-icons/io5";

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
    const [address, setAddress] = React.useState('');
    const [provDocID, setProvDocID] = React.useState('');
    const [province, setProvince] = React.useState('');
    const [boxHeight, setBoxHeight] = React.useState(400);
    const [boxWidth, setBoxWidth] = React.useState(350);
    const [showPassword, setShowPassword] = React.useState(false)

    const login = 'login'
    const signUp = 'signUp'
    const prescriber = 'Prescriber'
    const patient = 'Patient'
    const admin = 'Admin'
    const loginText = loginImage
    const navigate = useNavigate()

    const typeSwitchClicked = (buttonId) => {
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

    const loginClicked = async () => {

        try {
            if (activeButton === patient) {
                const response = await fetch('https://notparx-user-service.azurewebsites.net/api/loginUser/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
                });
                if (response.ok) {
                    console.log("Login Success")
                    navigate('/Patient')
                } else {
                  console.error("Login Fail");
                }
            } else if (activeButton === prescriber) {
                const response = await fetch('https://notparx-user-service.azurewebsites.net/api/loginPrescriber/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
                });
                if (response.ok) {
                    console.log("Login Success")
                    navigate('/Prescriber')
                } else {
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
                if (response.ok) {
                    console.log("Login Success")
                    navigate('/Admin')
                } else {
                  console.error("Login Fail");
                }
            }
          } catch (error) {
            console.error("Login Error");
          }
    }

    const signUpClicked = async () => {
        try {
            if (activeButton === patient) {
                const response = await fetch('https://notparx-user-service.azurewebsites.net/api/registerUser/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password, firstName, lastName, address, city, province, language, email })
                });
                if (response.ok) {
                    console.log("Patient Register Success")
                    navigate('/Patient')
                } else {
                  console.error("Patient Register Fail");
                }
            } else {
                const response = await fetch('https://notparx-user-service.azurewebsites.net/api/registerPrescriber/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ provDocID, password, address, city, language, email })
                });
                if (response.ok) {
                    console.log("Prescriber Register Success")
                    navigate('/Prescriber')
                } else {
                  console.error("Prescriber Register Fail");
                }
            }
          } catch (error) {
            console.error("Register Error");
          }
    }

    return (
        <div className='screen-container'>
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
                                        <div className='column'>
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
                                            <div style={{marginTop: `12px`}}>
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
                                        <div className='column'>
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
                                <input type="text" className="input-field" placeholder="Address" value={address} onChange={handleAddressChange}/>
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
                                <input
                                    type={showPassword ? 'text' : 'password'}
                                    className='input-field'
                                    placeholder="Password"
                                />
                                <button className='password-toggle-button' onClick={toggleShowPassword}>
                                    <IoEyeOutline/>
                                </button>
                            </div>
                            
                            
                            <div className='row'>
                            {currentView === signUp && (
                                <button className='custom-button' onClick={() => signUpClicked()}>
                                    <span>Get Started</span>
                                </button>
                            )}
                            {currentView === login && (
                                <button className='custom-button' onClick={() => loginClicked()}>
                                    <span>Get Started</span>
                                </button>
                            )}
                            </div> 
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