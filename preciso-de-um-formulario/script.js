document.addEventListener('DOMContentLoaded', () => {
  const cepInput = document.getElementById('cep');
  const spinner = document.getElementById('cep-spinner');
  const statusIcon = document.getElementById('cep-status');
  const errorMessage = document.getElementById('cep-error');
  const form = document.getElementById('address-form');
  const resultCard = document.getElementById('result-card');
  const resultText = document.getElementById('result-text');

  const addressFields = {
    logradouro: document.getElementById('logradouro'),
    bairro: document.getElementById('bairro'),
    cidade: document.getElementById('cidade'),
    estado: document.getElementById('estado'),
  };

  // Máscara de CEP: 99999-999
  cepInput.addEventListener('input', (e) => {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 5) {
      value = value.slice(0, 5) + '-' + value.slice(5, 8);
    }
    e.target.value = value;

    hideStatus();
    hideError();

    if (value.replace('-', '').length === 8) {
      fetchCep(value.replace('-', ''));
    }
  });

  // Permitir colar CEPs
  cepInput.addEventListener('paste', (e) => {
    setTimeout(() => {
      cepInput.dispatchEvent(new Event('input'));
    }, 10);
  });

  async function fetchCep(cep) {
    showSpinner();
    clearFields();

    try {
      const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);

      if (!response.ok) {
        throw new Error('Erro na conexão');
      }

      const data = await response.json();

      if (data.erro) {
        showError('CEP não encontrado. Verifique e tente novamente.');
        showStatusIcon('error');
        return;
      }

      fillFields(data);
      showStatusIcon('success');

      // Foca no campo número após preencher
      document.getElementById('numero').focus();

    } catch (err) {
      showError('Não foi possível consultar o CEP. Verifique sua conexão.');
      showStatusIcon('error');
    } finally {
      hideSpinner();
    }
  }

  function fillFields(data) {
    addressFields.logradouro.value = data.logradouro || '';
    addressFields.bairro.value = data.bairro || '';
    addressFields.cidade.value = data.localidade || '';
    addressFields.estado.value = data.uf || '';

    // Adiciona classe visual de preenchido
    Object.values(addressFields).forEach((field) => {
      if (field.value) {
        field.classList.add('filled');
      }
    });

    // Se logradouro veio vazio, libera para edição
    if (!data.logradouro) {
      addressFields.logradouro.removeAttribute('readonly');
      addressFields.logradouro.focus();
    }

    // Se bairro veio vazio, libera para edição
    if (!data.bairro) {
      addressFields.bairro.removeAttribute('readonly');
    }
  }

  function clearFields() {
    Object.values(addressFields).forEach((field) => {
      field.value = '';
      field.classList.remove('filled');
      if (field.id !== 'numero' && field.id !== 'complemento') {
        field.setAttribute('readonly', true);
      }
    });
    resultCard.classList.add('hidden');
  }

  function showSpinner() {
    spinner.classList.remove('hidden');
    statusIcon.classList.add('hidden');
  }

  function hideSpinner() {
    spinner.classList.add('hidden');
  }

  function showStatusIcon(type) {
    statusIcon.classList.remove('hidden', 'success', 'error');
    if (type === 'success') {
      statusIcon.textContent = '\u2714';
      statusIcon.classList.add('success');
    } else {
      statusIcon.textContent = '\u2718';
      statusIcon.classList.add('error');
    }
  }

  function hideStatus() {
    statusIcon.classList.add('hidden');
  }

  function showError(msg) {
    errorMessage.textContent = msg;
    errorMessage.classList.remove('hidden');
  }

  function hideError() {
    errorMessage.textContent = '';
    errorMessage.classList.add('hidden');
  }

  // Submit do formulário
  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const cep = cepInput.value.trim();
    const logradouro = addressFields.logradouro.value.trim();
    const numero = document.getElementById('numero').value.trim();
    const complemento = document.getElementById('complemento').value.trim();
    const bairro = addressFields.bairro.value.trim();
    const cidade = addressFields.cidade.value.trim();
    const estado = addressFields.estado.value.trim();

    if (!cep || !logradouro || !cidade || !estado) {
      showError('Preencha o CEP e aguarde o carregamento do endereço.');
      return;
    }

    const parts = [logradouro];
    if (numero) parts.push(numero);
    if (complemento) parts.push(complemento);
    parts.push(bairro);
    parts.push(`${cidade} - ${estado}`);
    parts.push(`CEP: ${cep}`);

    resultText.textContent = parts.join(', ');
    resultCard.classList.remove('hidden');

    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });
});
