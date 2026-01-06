import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const uploadDocument = async (files: FileList | File[], sessionId: string) => {
    const formData = new FormData();

    // Append each file with the key "files" (must match backend parameter name)
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }
    formData.append('session_id', sessionId);

    // Note: 'files' matches the python argument `files: list[UploadFile]`
    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const queryDocument = async (question: string, filenames: string[] = [], sessionId: string) => {
    const response = await axios.post(`${API_BASE_URL}/query`, { question, filenames, session_id: sessionId });
    return response.data;
};

export const resetSession = async (sessionId: string) => {
    const response = await axios.delete(`${API_BASE_URL}/reset/${sessionId}`);
    return response.data;
};

export const deleteFile = async (filename: string, sessionId: string) => {
    // Encode filename to handle spaces/special chars
    const encodedName = encodeURIComponent(filename);
    const response = await axios.delete(`${API_BASE_URL}/files/${sessionId}/${encodedName}`);
    return response.data;
};
