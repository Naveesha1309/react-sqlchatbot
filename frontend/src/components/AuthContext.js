import React, { createContext, useState } from 'react';

export const AuthContext = createContext();

const email = process.env.REACT_APP_ADMIN_EMAIL;
const password = process.env.REACT_APP_ADMIN_PASSWORD;

function AuthProvider({ children }) {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [error, setError] = useState('');

    const login = (enteredEmail, enteredPassword) => {
        if (enteredEmail===email && enteredPassword===password) {
            setIsLoggedIn(true);
            setError(''); // Clear error message on successful login
        } else {
            setIsLoggedIn(false);
            setError('Incorrect credentials, please try again.');
        }
    };

    return (
        <AuthContext.Provider value={{ isLoggedIn, login, error }}>
            {children}
        </AuthContext.Provider>
    );
}

export { AuthProvider };
