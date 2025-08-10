// Pure function: AxiosError -> { message, fieldErrors }
export function parseApiError(err) {
  const res = { message: 'An unexpected error occurred', fieldErrors: {} };

  const data = err?.response?.data;
  if (!data) return res;
  if (typeof data.detail === 'string') {
    res.message = data.detail;
  } else if (data.detail && typeof data.detail === 'object') {
    const msgs = [];
    for (const k of Object.keys(data.detail)) {
      const v = data.detail[k];
      const text = Array.isArray(v) ? v[0] : v;
      res.fieldErrors[k] = String(text);
      msgs.push(`${k}: ${text}`);
    }
    res.message = msgs.join(', ');
  } else if (data.message) {
    res.message = data.message;
  }
  return res;
}
