// components/ImageUploader.tsx
'use client'; // Add this line at the top
import React, { useState } from 'react';

const ImageUploader = () => {
    const [file, setFile] = useState<File | null>(null);
    const [responseImage, setResponseImage] = useState<string | null>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            setFile(event.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://127.0.0.1:5000/api/upload', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            if (response.ok) {
                // Assuming the returned image URL is part of the response
                setResponseImage(`http://127.0.0.1:5000/${data.detection_image}`);
            } else {
                console.error(data.error);
            }
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    return (
        <div style={{ margin: '20px 20px' }}>
            <h1 style={{ fontSize: '36px'}}>Animal Detection</h1>
            <h2>(1) Upload an image and (2) Push the Detect objects button.</h2>
            <input
                type="file"
                onChange={handleFileChange}
                style={{
                    marginBottom: '20px',
                    padding: '10px 20px',
                    backgroundColor: '#007BFF',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '5px',
                    cursor: 'pointer',
                    display: 'block'
                }}
            />
            <div>
                <button onClick={handleUpload} style={{ padding: '10px 20px', backgroundColor: '#007BFF', color: '#fff', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
                    Detect objects
                </button>
                <p>This action may take a few minutes.</p>
            </div>
            {responseImage && (
                <div>
                    <h2>Processed Image:</h2>
                    <p>
                        The processed image is available at:{' '}
                        <a href={responseImage} target="_blank" rel="noopener noreferrer">
                            {responseImage}
                        </a>
                    </p>
                    <img src={responseImage} alt="Processed" />
                </div>
            )}
        </div>
    );
};

export default ImageUploader;