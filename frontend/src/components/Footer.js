import React from 'react';

const Footer = () => {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="bg-navbar text-white py-4">
            <div className="container mx-auto flex flex-col items-center">
                <p>&copy; {currentYear} Your Company. All rights reserved.</p>
                {/* <div className="flex space-x-4">
                    <a href="/privacy-policy" className="text-gray-400 hover:text-white">Privacy Policy</a>
                    <a href="/terms-of-service" className="text-gray-400 hover:text-white">Terms of Service</a>
                    <a href="/contact-us" className="text-gray-400 hover:text-white">Contact Us</a>
                </div> */}
            </div>
        </footer>
    );
};

export default Footer;
