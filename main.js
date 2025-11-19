document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const patientList = document.getElementById('patientList');
    const noResults = document.getElementById('noResults');
    const defaultAvatar = '/static/uploads/default.png';

    // Função para renderizar a lista de pacientes
    const renderPatients = (patients) => {
        patientList.innerHTML = '';
        if (patients.length === 0) {
            noResults.style.display = 'block';
        } else {
            noResults.style.display = 'none';
            patients.forEach(patient => {
                const patientPhoto = patient.foto_path ? `/static/${patient.foto_path}` : defaultAvatar;
                
                const patientItem = `
                    <a href="/paciente/${patient.id}" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                        <div class="d-flex align-items-center">
                            <img src="${patientPhoto}" alt="Foto de ${patient.nome_completo}" class="rounded-circle me-3" style="width: 50px; height: 50px; object-fit: cover;">
                            <div>
                                <h5 class="mb-1">${patient.nome_completo}</h5>
                                <p class="mb-1 text-muted">CPF: ${patient.cpf || 'Não informado'} | Telefone: ${patient.telefone || 'Não informado'}</p>
                            </div>
                        </div>
                    </a>
                `;
                patientList.insertAdjacentHTML('beforeend', patientItem);
            });
        }
    };

    // Função para buscar pacientes
    const fetchPatients = async (query = '') => {
        try {
            const response = await fetch(`/api/pesquisar_pacientes?q=${encodeURIComponent(query)}`);
            const patients = await response.json();
            renderPatients(patients);
        } catch (error) {
            console.error('Erro ao buscar pacientes:', error);
            patientList.innerHTML = '<p class="text-danger text-center">Ocorreu um erro ao carregar os pacientes.</p>';
        }
    };

    // Event listener para o campo de busca
    if (searchInput) {
        searchInput.addEventListener('input', () => fetchPatients(searchInput.value));
        // Carrega todos os pacientes inicialmente
        fetchPatients();
    }
});