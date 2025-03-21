 const dropArea = document.getElementById('drop-area');
 const inputFile = document.getElementById('input-file');
 
 // Prevent default drag behaviors
 ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
     dropArea.addEventListener(eventName, preventDefaults, false);
     document.body.addEventListener(eventName, preventDefaults, false);
 });
 
 // Highlight drop area when item is dragged over it
 ['dragenter', 'dragover'].forEach(eventName => {
     dropArea.addEventListener(eventName, highlight, false);
 });
 
 ['dragleave', 'drop'].forEach(eventName => {
     dropArea.addEventListener(eventName, unhighlight, false);
 });
 
 // Handle dropped files
 dropArea.addEventListener('drop', handleDrop, false);
 
 // Handle file input changes (when user selects file through dialog)
 inputFile.addEventListener('change', handleFiles, false);
 
 function preventDefaults(e) {
     e.preventDefault();
     e.stopPropagation();
 }
 
 function highlight() {
     dropArea.classList.add('highlight');
 }
 
 function unhighlight() {
     dropArea.classList.remove('highlight');
 }
 
 function handleDrop(e) {
     const dt = e.dataTransfer;
     const files = dt.files;
     handleFiles(files);
 }
 
 function handleFiles(e) {
     let files;
     if (e.dataTransfer) {
         files = e.dataTransfer.files;
     } else if (e.target && e.target.files) {
         files = e.target.files;
     } else {
         files = e;
     }
     
     if (files.length) {
         const file = files[0];
         
         // Check if file is a PDF
         if (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')) {
             console.log('PDF file selected:', file.name);
             
             // You could add code here to:
             // 1. Read the file using FileReader
             // 2. Send the file to a backend service
             // 3. Process the PDF with pdf.js or similar library
             
             // Show filename in the UI
             document.querySelector('#img-view p').textContent = `Selected: ${file.name}`;
         } else {
             alert('Please select a PDF file');
         }
     }
 }