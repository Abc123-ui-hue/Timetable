// HealthCare Hospital - Data module
// Provides departments, doctors, and timeslots for demo purposes

window.hospitalData = {
  departments: [
    { id: 'cardiology', name: 'Cardiology' },
    { id: 'neurology', name: 'Neurology' },
    { id: 'orthopedics', name: 'Orthopedics' },
    { id: 'pediatrics', name: 'Pediatrics' },
    { id: 'dermatology', name: 'Dermatology' },
    { id: 'oncology', name: 'Oncology' }
  ],
  doctors: [
    { id: 'd1', name: 'Dr. Alice Brown', departmentId: 'cardiology', title: 'Senior Cardiologist', languages: ['English', 'Spanish'], experienceYears: 14 },
    { id: 'd2', name: 'Dr. Brian Chen', departmentId: 'neurology', title: 'Consultant Neurologist', languages: ['English', 'Mandarin'], experienceYears: 11 },
    { id: 'd3', name: 'Dr. Carla Gomez', departmentId: 'orthopedics', title: 'Orthopedic Surgeon', languages: ['English'], experienceYears: 9 },
    { id: 'd4', name: 'Dr. Daniel Singh', departmentId: 'pediatrics', title: 'Pediatrician', languages: ['English', 'Hindi'], experienceYears: 12 },
    { id: 'd5', name: 'Dr. Elena Petrova', departmentId: 'dermatology', title: 'Dermatologist', languages: ['English', 'Russian'], experienceYears: 8 },
    { id: 'd6', name: 'Dr. Faisal Ahmed', departmentId: 'oncology', title: 'Oncologist', languages: ['English', 'Arabic'], experienceYears: 15 }
  ],
  timeslots: [
    '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
    '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
    '16:00'
  ]
};
