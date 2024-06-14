import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

const email = process.env.REACT_APP_ADMIN_EMAIL;
const password = process.env.REACT_APP_ADMIN_PASSWORD;

function AuthProvider({ children }) {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        const loggedInStatus = localStorage.getItem('isLoggedIn');
        setIsLoggedIn(loggedInStatus === 'true');
    }, []);

    const login = (enteredEmail, enteredPassword) => {
        if (enteredEmail === email && enteredPassword === password) {
            setIsLoggedIn(true);
            setError('');  //clear msg after login success
            localStorage.setItem('isLoggedIn', 'true');
        } else {
            setIsLoggedIn(false);
            setError('Incorrect credentials, please try again.');
            localStorage.setItem('isLoggedIn', 'false');
        }
    };

    const logout = () => {
        setIsLoggedIn(false);
        localStorage.setItem('isLoggedIn', 'false');
    };

    return (
        <AuthContext.Provider value={{ isLoggedIn, login, logout, error }}>
            {children}
        </AuthContext.Provider>
    );
}

export { AuthProvider };
