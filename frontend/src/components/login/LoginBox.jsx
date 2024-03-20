import './LoginBox.scss';
import { Button } from '@mui/material';
import * as React from 'react';
import loginImage from '../../resources/img/LoginText.png';
import { useNavigate } from 'react-router-dom';

const LoginBox = () => {

    const [activeButton, setActiveButton] = React.useState('Patient');

    const handleButtonClick = (buttonId) => {
        setActiveButton(buttonId);
    };

    const getActiveButton = () => {
        return activeButton
    }

    const [username, setUsername] = React.useState('');
    const [password, setPassword] = React.useState('');

    const loginText = loginImage
    const navigate = useNavigate()

    const loginClicked = async () => {

        try {
            if (activeButton == "Patient") {
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
            } else if (activeButton == "Prescriber") {
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

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    }

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    }

    return (
        <div className='screen-container'>
            <div className='image-container'>
                <img src={loginText} />
            </div>

            <div className='login-component'>
                <div className='content'>
                    <div className='table-container'>
                        <h2>Log in</h2>
                        <p>Who are you?</p>
                        <div className='button-group'>
                            <button
                                className={`type-button ${activeButton === 'Patient' ? 'active' : ''}`}
                                onClick={() => handleButtonClick('Patient')} >
                                Patient
                            </button>
                            <button
                                className={`type-button ${activeButton === 'Prescriber' ? 'active' : ''}`}
                                onClick={() => handleButtonClick('Prescriber')} >
                                Prescriber
                            </button>
                            <button
                                className={`type-button ${activeButton === 'Admin' ? 'active' : ''}`}
                                onClick={() => handleButtonClick('Admin')} >
                                Admin
                            </button>
                        </div>

                        <p>Username</p>
                        <input type="text" className="input-field" placeholder="Username" value={username} onChange={handleUsernameChange}/>
                        <p>Password</p>
                        <input type="text" className="input-field" placeholder="Password" value={password} onChange={handlePasswordChange}/>
                        <div className='row'>
                            <button className='custom-button' onClick={() => loginClicked()}>
                                <span>Get Started</span>
                            </button>
                        </div> 
                        <div className='row'>
                            <button className='switch-screen-button'>
                                <span>Create a new account</span>
                            </button>
                        </div> 
                        


                    </div>
                </div>
            </div>
        </div>
        
    );
};

export default LoginBox;