import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

const Uploader = ({ onFileUpload }) => {
    const onDrop = useCallback((acceptedFiles) => {
        if (acceptedFiles.length > 0) {
            onFileUpload(acceptedFiles[0]);
        }
    }, [onFileUpload]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
        },
        multiple: false,
    });

    return (
        <section className="uploader">
            <div {...getRootProps({ className: `dropzone ${isDragActive ? 'active' : ''}` })}>
                <input {...getInputProps()} />
                <div id="upload-icon">⬆️</div>
                <span id="upload-text">
                    {isDragActive ? 'Drop the PDF here...' : 'Click to browse or drag & drop a PDF'}
                </span>
            </div>
        </section>
    );
};

export default Uploader;