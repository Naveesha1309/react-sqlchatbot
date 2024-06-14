import { useContext, useEffect, useState , useMemo} from 'react';
import { AuthContext } from '../components/AuthContext';


export default function Login() {
    const { login, error } = useContext(AuthContext);
    const [currentText, setCurrentText] = useState('');
    const textArray = useMemo(() => [
        "Welcome to Database Chatbot!",
        "Chat with your database effortlessly.",
        "Your data, your questions, instant answers."
    ], []);
    const speed = 2000; // Change text every 2 seconds

    useEffect(() => {
        let index = 0;
        const interval = setInterval(() => {
            setCurrentText(textArray[index]);
            index = (index + 1) % textArray.length;
        }, speed);

        return () => clearInterval(interval);
    }, [textArray, speed]);

    const handleSubmit = (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const email = formData.get('email');
        const password = formData.get('password');
        login(email, password);
    };

    return (
        <div className="relative flex items-center justify-center min-h-screen bg-cover bg-center" style={{ backgroundImage: 'url(https://images.pexels.com/photos/8721318/pexels-photo-8721318.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2)' }}>
            <div className="absolute top-0 left-0 w-3/4 h-full flex flex-col items-start p-8 bg-opacity-55 bg-gray-900 text-white pt-56">
                <h1 className="text-4xl font-bold mb-4" style={{ fontFamily: 'Cinzel, serif' }}>Database Chatbot</h1>
                <p className="text-2xl"  style={{ fontFamily: 'Cinzel, serif' }}>{currentText}</p>
            </div>
            <div className="w-full max-w-md p-8 space-y-6 bg-login-color rounded-lg shadow-lg z-10 ml-auto mr-8">
                <h2 className="text-2xl font-bold text-center text-gray-900"  style={{ fontFamily: 'Cinzel, serif' }}>Admin Login</h2>
                {error && (
                    <div className="text-red-600 text-center">
                        {error}
                    </div>
                )}
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-700"  style={{ fontFamily: 'Cinzel, serif' }}>Email</label>
                        <input
                            type="text"
                            name="email"
                            id="email"
                            required
                            className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                        />
                    </div>
                    <div>
                        <label htmlFor="password" className="block text-sm font-medium text-gray-700"  style={{ fontFamily: 'Cinzel, serif' }}>Password</label>
                        <input
                            type="password"
                            name="password"
                            id="password"
                            required
                            className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                        />
                    </div>
                    <div>
                        <button
                            type="submit"
                            className="w-full px-4 py-2 bg-login-color-button-hover rounded-md shadow hover:bg-login-color-button-hover-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"  style={{ fontFamily: 'Cinzel, serif' }}
                        >
                            Login
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
