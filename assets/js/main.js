// HealthCare Hospital - Main JS

(function () {
  function onReady(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  async function loadComponent(targetSelector, path, onLoad) {
    const target = document.querySelector(targetSelector);
    if (!target) return;
    try {
      const res = await fetch(path, { cache: 'no-cache' });
      if (!res.ok) throw new Error('Failed to load ' + path);
      const html = await res.text();
      target.innerHTML = html;
      if (typeof onLoad === 'function') onLoad();
    } catch (err) {
      console.warn('[component]', err.message);
    }
  }

  function setupHeaderInteractions() {
    const nav = document.getElementById('primary-nav');
    const toggle = document.getElementById('nav-toggle');
    if (!nav || !toggle) return;
    toggle.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(isOpen));
    });

    // Highlight active link
    const links = nav.querySelectorAll('a[href]');
    const current = normalizePath(location.pathname);
    for (const link of links) {
      const href = normalizePath(link.getAttribute('href') || '');
      if (href === current || (current === 'index.html' && href === 'index.html')) {
        link.classList.add('current');
        link.setAttribute('aria-current', 'page');
      }
    }
  }

  function setupFooterYear() {
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = String(new Date().getFullYear());
  }

  function normalizePath(p) {
    if (!p) return '';
    const parts = p.split('/').filter(Boolean);
    if (parts.length === 0) return 'index.html';
    const last = parts[parts.length - 1];
    return last || 'index.html';
  }

  // Doctors page: filtering + rendering
  function initDoctorsDirectory() {
    const grid = document.getElementById('doctor-grid');
    const search = document.getElementById('doctor-search');
    const deptFilter = document.getElementById('department-filter');
    if (!grid || !window.hospitalData) return; // Not on doctors page

    const { doctors = [], departments = [] } = window.hospitalData;
    // Populate department select
    if (deptFilter && departments.length) {
      deptFilter.innerHTML = '<option value="">All departments</option>' +
        departments.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
    }

    function render(list) {
      grid.innerHTML = list.map(d => `
        <article class="card doctor-card" data-name="${d.name.toLowerCase()}" data-dept="${d.departmentId}">
          <div class="doctor-avatar"><img src="assets/img/doctor-placeholder.svg" alt="${d.name}" width="72" height="72"></div>
          <div>
            <h3>${d.name}</h3>
            <div class="doctor-meta">${lookupDepartmentName(d.departmentId, departments)} • ${d.title}</div>
            <div class="text-muted">${d.experienceYears}+ yrs • ${d.languages.join(', ')}</div>
          </div>
        </article>
      `).join('');
    }

    function lookupDepartmentName(id, deps) {
      const m = deps.find(x => x.id === id);
      return m ? m.name : '—';
    }

    function applyFilter() {
      const q = (search && search.value || '').trim().toLowerCase();
      const dept = deptFilter ? deptFilter.value : '';
      const filtered = doctors.filter(d => {
        const okQ = !q || d.name.toLowerCase().includes(q) || (d.title || '').toLowerCase().includes(q);
        const okDept = !dept || d.departmentId === dept;
        return okQ && okDept;
      });
      render(filtered);
    }

    // Initial render
    render(doctors);
    if (search) search.addEventListener('input', applyFilter);
    if (deptFilter) deptFilter.addEventListener('change', applyFilter);
  }

  // Appointment form
  function initAppointmentForm() {
    const deptSelect = document.getElementById('department-select');
    const doctorSelect = document.getElementById('doctor-select');
    const timeSelect = document.getElementById('time-select');
    const form = document.getElementById('appointment-form');
    const success = document.getElementById('appointment-success');
    const error = document.getElementById('appointment-error');
    if (!form || !window.hospitalData) return; // Not on appointment page

    const { departments = [], doctors = [], timeslots = [] } = window.hospitalData;
    // Populate departments
    if (deptSelect) {
      deptSelect.innerHTML = '<option value="">Select department</option>' +
        departments.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
    }
    // Populate times
    if (timeSelect) {
      timeSelect.innerHTML = '<option value="">Select time</option>' +
        timeslots.map(t => `<option value="${t}">${t}</option>`).join('');
    }
    // Chain doctors
    function populateDoctors(deptId) {
      if (!doctorSelect) return;
      const list = doctors.filter(d => !deptId || d.departmentId === deptId);
      doctorSelect.innerHTML = '<option value="">Select doctor</option>' +
        list.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
    }
    populateDoctors('');
    if (deptSelect) deptSelect.addEventListener('change', () => populateDoctors(deptSelect.value));

    // Validation + fake submit
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const required = ['patient-name', 'patient-phone', 'department', 'doctor', 'date', 'time'];
      const missing = required.filter(k => !(data.get(k) || '').toString().trim());
      if (missing.length) {
        if (error) { error.style.display = 'block'; error.textContent = 'Please fill all required fields.'; }
        if (success) success.style.display = 'none';
        return;
      }
      if (success) { success.style.display = 'block'; success.textContent = 'Your appointment request was submitted successfully. We will contact you shortly.'; }
      if (error) error.style.display = 'none';
      form.reset();
      populateDoctors('');
    });
  }

  onReady(() => {
    loadComponent('#site-header', 'components/header.html', () => {
      setupHeaderInteractions();
    });
    loadComponent('#site-footer', 'components/footer.html', () => {
      setupFooterYear();
    });
    initDoctorsDirectory();
    initAppointmentForm();
  });
})();
