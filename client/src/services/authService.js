import api from './api';

export const loginUser = async (email, password) => {
  try {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to login');
  }
};

export const registerUser = async (name, email, password) => {
  try {
    const response = await api.post('/auth/register', { name, email, password });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to register');
  }
};

export const getCurrentUser = async () => {
  try {
    const response = await api.get('/auth/me');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to get user data');
  }
};

export const loginWithGoogle = async (tokenId) => {
  try {
    const response = await api.post('/auth/google', { token_id: tokenId });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to login with Google');
  }
};
