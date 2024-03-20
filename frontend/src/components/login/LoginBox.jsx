import './LoginBox.scss';
import * as React from 'react';
import loginImage from '../../resources/img/LoginText.png';
import { useNavigate } from 'react-router-dom';

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
    const [province, setProvince] = React.useState('')


    const login = 'login'
    const signUp = 'signUp'
    const prescriber = 'Prescriber'
    const patient = 'Patient'
    const admin = 'Admin'
    const loginText = loginImage
    const navigate = useNavigate()

    const typeSwitchClicked = (buttonId) => {
        setActiveButton(buttonId);
    };

    const switchViewClicked = (buttonID) => {
        if (buttonID === 'login') {
            setCurrentView('signUp')
        } else {
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
                        <div className='table-container'>
                            {currentView === login && (<h2>Log in</h2>)}
                            {currentView === signUp && (<h2>Sign Up</h2>)}
                            <p>Who are you?</p>
                            <div className='button-group'>
                                <button
                                    className={`type-button ${activeButton === patient ? 'active' : ''}`}
                                    onClick={() => typeSwitchClicked(patient)} >
                                    Patient
                                </button>
                                <button
                                    className={`type-button ${activeButton === prescriber ? 'active' : ''}`}
                                    onClick={() => typeSwitchClicked(prescriber)} >
                                    Prescriber
                                </button>
                                {currentView === login && (
                                    <button
                                        className={`type-button ${activeButton === admin ? 'active' : ''}`}
                                        onClick={() => typeSwitchClicked(admin)} >
                                        Admin
                                    </button>
                                )}
                            </div>
                            {currentView === signUp && (
                                <>
                                {activeButton === prescriber && (
                                    <>
                                    <p>Unique PaRx ID</p>
                                    <input type="text" className="input-field" placeholder="Unique PaRx ID" value={provDocID} onChange={handleProvDocIDChange}/>
                                    </>
                                )}

                                {activeButton === patient && (
                                    <>
                                    <p>First Name</p>
                                    <input type="text" className="input-field" placeholder="First Name" value={firstName} onChange={handleFirstNameChange}/>
                                    <p>Last Name</p>
                                    <input type="text" className="input-field" placeholder="Last Name" value={lastName} onChange={handleLastNameChange}/>
                                    </>
                                )}
                                <p>Email</p>
                                <input type="text" className="input-field" placeholder="Email" value={email} onChange={handleEmailChange}/>
                                <p>Language</p>
                                <input type="text" className="input-field" placeholder="Language" value={language} onChange={handleLanguageChange}/>
                                {activeButton === patient && (
                                    <>
                                    <p>Province</p>
                                    <input type="text" className="input-field" placeholder="Province" value={province} onChange={handleProvinceChange}/>
                                    </>
                                )}
                                <p>City</p>
                                <input type="text" className="input-field" placeholder="City" value={city} onChange={handleCityChange}/>
                                <p>Address</p>
                                <input type="text" className="input-field" placeholder="Address" value={address} onChange={handleAddressChange}/>
                                </>
                            )}
                            {(currentView === login || (currentView === signUp && activeButton === patient)) && (
                                <>
                                <p>Username</p>
                                <input type="text" className="input-field" placeholder="Username" value={username} onChange={handleUsernameChange}/>
                                </>
                            )}
                            <p>Password</p>
                            <input type="text" className="input-field" placeholder="Password" value={password} onChange={handlePasswordChange}/>
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


// {currentView === 'signUp' && (
//     <div className='content'>
//         <div className='table-container'>
//             <h2>Sign Up</h2>
//             <p>Who are you?</p>
//             <div className='button-group'>
//                 <button
//                     className={`type-button ${activeButton === 'Patient' ? 'active' : ''}`}
//                     onClick={() => typeSwitchClicked('Patient')} >
//                     Patient
//                 </button>
//                 <button
//                     className={`type-button ${activeButton === 'Prescriber' ? 'active' : ''}`}
//                     onClick={() => typeSwitchClicked('Prescriber')} >
//                     Prescriber
//                 </button>
//             </div>

//             <p>Username</p>
//             <input type="text" className="input-field" placeholder="Username" value={username} onChange={handleUsernameChange}/>
//             <p>Password</p>
//             <input type="text" className="input-field" placeholder="Password" value={password} onChange={handlePasswordChange}/>
//             <div className='row'>
//                 <button className='custom-button' onClick={() => loginClicked()}>
//                     <span>Get Started</span>
//                 </button>
//             </div> 
//             <div className='row'>
//                 <button className='switch-screen-button' onClick={() => switchViewClicked('signUp')}>
//                     <span>Use an existing account</span>
//                 </button>
//             </div> 
//         </div>
//     </div>
// )}