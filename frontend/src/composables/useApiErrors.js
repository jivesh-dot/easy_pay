import { ref } from 'vue';
import { parseApiError } from '../utils/parseApiError';

export function useApiErrors() {
  const message = ref('');
  const fieldErrors = ref({});  // { email: 'already exists', password: 'too short', ... }

  function fromAxios(err) {
    const { message: msg, fieldErrors: fields } = parseApiError(err);
    message.value = msg;
    fieldErrors.value = fields;
  }
  function reset() {
    message.value = '';
    fieldErrors.value = {};
  }
  return { message, fieldErrors, fromAxios, reset };
}