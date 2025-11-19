// Main JavaScript for Osteopatia Manager

$(document).ready(function() {
    // Initialize components
    initializeDatePickers();
    initializeFormValidation();
    initializeFileUpload();
    initializeMasks();
    initializeTooltips();
    
    // Initialize search if on the correct page
    if ($('#searchInput').length) {
        initializeLiveSearch();
    }

    // Add fade-in animation to cards
    $('.card').addClass('fade-in');
});

// Initialize Flatpickr date pickers
function initializeDatePickers() {
    // Date picker for birth date and other dates
    flatpickr('.date-picker', {
        locale: 'pt',
        dateFormat: 'd/m/Y',
        allowInput: true,
        maxDate: 'today'
    });
    
    // Date picker for return dates (future dates allowed)
    flatpickr('.future-date-picker', {
        locale: 'pt',
        dateFormat: 'd/m/Y',
        allowInput: true,
        minDate: 'today'
    });
}

// Initialize form validation
function initializeFormValidation() {
    // CPF validation
    $('.cpf-input').on('blur', function() {
        const cpf = $(this).val().replace(/\D/g, '');
        if (cpf && !validateCPF(cpf)) {
            $(this).addClass('is-invalid');
            $(this).siblings('.invalid-feedback').text('CPF inválido');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
    
    // Email validation
    $('.email-input').on('blur', function() {
        const email = $(this).val();
        if (email && !validateEmail(email)) {
            $(this).addClass('is-invalid');
            $(this).siblings('.invalid-feedback').text('Email inválido');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
    
    // Required field validation
    $('.required-field').on('blur', function() {
        if (!$(this).val().trim()) {
            $(this).addClass('is-invalid');
            $(this).siblings('.invalid-feedback').text('Este campo é obrigatório');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
    
    // Form submission validation
    $('form').on('submit', function(e) {
        let isValid = true;
        
        // Check required fields
        $(this).find('.required-field').each(function() {
            if (!$(this).val().trim() && !$(this).hasClass('cpf-input')) {
                $(this).addClass('is-invalid');
                $(this).siblings('.invalid-feedback').text('Este campo é obrigatório');
                isValid = false;
            }
        });
        
        // Check CPF
        $(this).find('.cpf-input').each(function() {
            const cpf = $(this).val().replace(/\D/g, '');
            if (cpf && !validateCPF(cpf)) {
                $(this).addClass('is-invalid');
                $(this).siblings('.invalid-feedback').text('CPF inválido');
                isValid = false;
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        // Check email
        $(this).find('.email-input').each(function() {
            const email = $(this).val();
            if (email && !validateEmail(email)) {
                $(this).addClass('is-invalid');
                $(this).siblings('.invalid-feedback').text('Email inválido');
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showAlert('Por favor, corrija os erros no formulário', 'error');
            // Scroll to first error
            $('html, body').animate({
                scrollTop: $('.is-invalid').first().offset().top - 100
            }, 500);
        }
    });
}

// Initialize file upload
function initializeFileUpload() {
    $('.file-upload-input').on('change', function() {
        const file = this.files[0];
        const label = $(this).siblings('.file-upload-label');
        const preview = $(this).closest('.file-upload-wrapper').find('.image-preview');
        
        if (file) {
            // Validate file type
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
            if (!allowedTypes.includes(file.type)) {
                showAlert('Tipo de arquivo não permitido. Use apenas JPG, PNG ou GIF.', 'error');
                $(this).val('');
                return;
            }
            
            // Validate file size (max 5MB)
            if (file.size > 5 * 1024 * 1024) {
                showAlert('Arquivo muito grande. Tamanho máximo: 5MB.', 'error');
                $(this).val('');
                return;
            }
            
            // Update label
            label.addClass('has-file');
            label.html(`<i class="fas fa-check-circle me-2"></i>${file.name}`);
            
            // Show preview
            if (preview.length) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.attr('src', e.target.result).show();
                };
                reader.readAsDataURL(file);
            }
        } else {
            label.removeClass('has-file');
            label.html('<i class="fas fa-cloud-upload-alt me-2"></i>Clique para selecionar uma foto');
            preview.hide();
        }
    });
}

// Initialize input masks
function initializeMasks() {
    // CPF mask
    $('.cpf-input').on('input', function() {
        let value = $(this).val().replace(/\D/g, '');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
        $(this).val(value);
    });
    
    // Phone mask
    $('.phone-input').on('input', function() {
        let value = $(this).val().replace(/\D/g, '');
        if (value.length <= 10) {
            value = value.replace(/(\d{2})(\d)/, '($1) $2');
            value = value.replace(/(\d{4})(\d)/, '$1-$2');
        } else {
            value = value.replace(/(\d{2})(\d)/, '($1) $2');
            value = value.replace(/(\d{5})(\d)/, '$1-$2');
        }
        $(this).val(value);
    });
    
    // Age input (numbers only)
    $('.age-input').on('input', function() {
        $(this).val($(this).val().replace(/\D/g, ''));
    });
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// CPF validation function
function validateCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    
    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) {
        return false;
    }
    
    let sum = 0;
    for (let i = 0; i < 9; i++) {
        sum += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let remainder = 11 - (sum % 11);
    if (remainder === 10 || remainder === 11) remainder = 0;
    if (remainder !== parseInt(cpf.charAt(9))) return false;
    
    sum = 0;
    for (let i = 0; i < 10; i++) {
        sum += parseInt(cpf.charAt(i)) * (11 - i);
    }
    remainder = 11 - (sum % 11);
    if (remainder === 10 || remainder === 11) remainder = 0;
    if (remainder !== parseInt(cpf.charAt(10))) return false;
    
    return true;
}

// Email validation function
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Show alert function
function showAlert(message, type = 'info') {
    const alertClass = type === 'error' ? 'alert-danger' : `alert-${type}`;
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Remove existing alerts
    $('.alert').remove();
    
    // Add new alert at the top of the page
    $('main.container').prepend(alertHtml);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut();
    }, 5000);
}

// Confirm delete function
function confirmDelete(message = 'Tem certeza que deseja excluir este item?') {
    return confirm(message);
}

// Loading spinner functions
function showLoading() {
    $('.loading-spinner').show();
}

function hideLoading() {
    $('.loading-spinner').hide();
}

// Search functionality
function initializeLiveSearch() {
    const searchInput = $('#searchInput');
    const patientList = $('#patientList');
    const loadingState = $('#loadingState');
    const noResultsState = $('#noResultsState');
    let searchTimeout;

    const renderPatients = (patients) => {
        patientList.empty();
        if (patients.length === 0) {
            noResultsState.show();
        } else {
            noResultsState.hide();
            patients.forEach(paciente => {
                const fotoUrl = paciente.foto_path 
                    ? `/static/uploads/${paciente.foto_path}` 
                    : `/static/uploads/default.png`; // Assuming you have a default avatar

                const pacienteHtml = `
                    <div class="search-result-item">
                        <div class="row align-items-center">
                            <div class="col-md-1 text-center">
                                <img src="${fotoUrl}" alt="Foto de ${paciente.nome_completo}" class="patient-avatar">
                            </div>
                            <div class="col-md-5">
                                <h6 class="mb-1">${paciente.nome_completo}</h6>
                                <p class="mb-1 text-muted">
                                    <i class="fas fa-id-card me-1"></i>CPF: ${paciente.cpf ? formatCpf(paciente.cpf) : 'Não informado'}
                                </p>
                                ${paciente.telefone ? `<p class="mb-0 text-muted"><i class="fas fa-phone me-1"></i>${formatPhone(paciente.telefone)}</p>` : ''}
                            </div>
                            <div class="col-md-3 text-center">
                                <small class="text-muted">
                                    <i class="fas fa-calendar me-1"></i>
                                    Cadastrado em<br>
                                    ${paciente.data_registro}
                                </small>
                            </div>
                            <div class="col-md-3 text-end">
                                <div class="btn-group" role="group">
                                    <a href="/paciente/${paciente.id}" class="btn btn-primary btn-sm" title="Ver Perfil">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    <a href="/novo-tratamento/${paciente.id}" class="btn btn-success btn-sm" title="Novo Tratamento">
                                        <i class="fas fa-plus"></i>
                                    </a>
                                    <a href="/editar-paciente/${paciente.id}" class="btn btn-info btn-sm" title="Editar Paciente">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                patientList.append(pacienteHtml);
            });
        }
    };

    const fetchPatients = (query) => {
        loadingState.show();
        noResultsState.hide();
        patientList.empty();

        $.ajax({
            url: '/api/pesquisar-pacientes',
            type: 'GET',
            data: { q: query },
            dataType: 'json',
            success: function(data) {
                renderPatients(data);
            },
            error: function() {
                patientList.html('<div class="alert alert-danger text-center">Erro ao buscar pacientes. Tente novamente.</div>');
            },
            complete: function() {
                loadingState.hide();
            }
        });
    };

    $('#searchInput').on('input', function() {
        const searchTerm = $(this).val().trim();
        clearTimeout(searchTimeout);
        
        searchTimeout = setTimeout(() => {
            fetchPatients(searchTerm);
        }, 300); // Debounce de 300ms para evitar muitas requisições
    });

    // Carrega todos os pacientes inicialmente
    fetchPatients('');

    // Foco automático no campo de busca
    searchInput.focus();
}

// Print function
function printPage() {
    window.print();
}

// Export to CSV function (placeholder)
function exportToCSV() {
    showAlert('Funcionalidade de exportação em desenvolvimento', 'info');
}

// Auto-save form data to localStorage
function autoSaveForm(formId) {
    const form = $(`#${formId}`);
    const formData = {};
    
    form.find('input, textarea, select').each(function() {
        const field = $(this);
        const name = field.attr('name');
        if (name && field.attr('type') !== 'file') {
            formData[name] = field.val();
        }
    });
    
    localStorage.setItem(`form_${formId}`, JSON.stringify(formData));
}

// Restore form data from localStorage
function restoreFormData(formId) {
    const savedData = localStorage.getItem(`form_${formId}`);
    if (savedData) {
        const formData = JSON.parse(savedData);
        const form = $(`#${formId}`);
        
        Object.keys(formData).forEach(function(name) {
            const field = form.find(`[name="${name}"]`);
            if (field.length) {
                field.val(formData[name]);
            }
        });
    }
}

// Clear saved form data
function clearSavedFormData(formId) {
    localStorage.removeItem(`form_${formId}`);
}

// Initialize auto-save for forms
$(document).ready(function() {
    $('form[data-auto-save]').each(function() {
        const formId = $(this).attr('id');
        if (formId) {
            // Restore data on page load
            restoreFormData(formId);
            
            // Save data on input change
            $(this).on('input change', function() {
                autoSaveForm(formId);
            });
            
            // Clear saved data on successful submit
            $(this).on('submit', function() {
                setTimeout(function() {
                    clearSavedFormData(formId);
                }, 1000);
            });
        }
    });
});

// Funções de formatação para uso no JS
function formatCpf(cpf) {
    if (!cpf) return '';
    cpf = cpf.replace(/\D/g, '');
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

function formatPhone(phone) {
    if (!phone) return '';
    phone = phone.replace(/\D/g, '');
    if (phone.length === 11) {
        return phone.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    }
    return phone.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
}
