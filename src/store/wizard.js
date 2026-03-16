import { defineStore } from 'pinia'

const STORAGE_KEY = 'upao_wizard_state'

const defaultState = () => ({
  step1: {
    domain: '',
    subline: ''
  },
  step2: {
    level: ''
  },
  step3: {
    scopeType: 'single',
    accessConfirmed: false,
    companyType: 'privada',
    name: '',
    count: null,
    description: '',
    sector: '',
    customSector: '',
    problem: ''
  },
  step4: {
    selectedTitles: [],
    proposals: [],
    sessionId: '',
    status: 'idle',
    error: ''
  }
})

// Load from localStorage on startup
const loadFromStorage = () => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) return JSON.parse(saved)
  } catch {}
  return defaultState()
}

export const useWizardStore = defineStore('wizard', {
  state: () => loadFromStorage(),

  getters: {
    isStep1Complete: (state) => !!(state.step1.domain && state.step1.subline),
    isStep2Complete: (state) => !!state.step2.level,
    isStep3Complete: (state) => !!(
      state.step3.accessConfirmed &&
      state.step3.name &&
      state.step3.sector &&
      (state.step3.sector !== 'otro' || state.step3.customSector) &&
      state.step3.problem
    ),

    // Returns the furthest step completed so we know where to resume
    lastCompletedStep: (state) => {
      const s1 = !!(state.step1.domain && state.step1.subline)
      const s2 = !!state.step2.level
      const s3 = !!(
        state.step3.accessConfirmed &&
        state.step3.name &&
        state.step3.sector &&
        (state.step3.sector !== 'otro' || state.step3.customSector) &&
        state.step3.problem
      )
      if (s3) return 4
      if (s2) return 3
      if (s1) return 2
      return 1
    },

    hasProgress: (state) => !!(state.step1.domain || state.step1.subline)
  },

  actions: {
    setStep1(domain, subline) {
      this.step1.domain = domain
      this.step1.subline = subline
      this._persist()
    },
    setStep2(level) {
      this.step2.level = level
      this._persist()
    },
    setStep3(data) {
      this.step3 = { ...this.step3, ...data }
      this._persist()
    },
    setStep4Selected(titles) {
      this.step4.selectedTitles = titles
      this._persist()
    },
    startProposalGeneration() {
      this.step4.proposals = []
      this.step4.selectedTitles = []
      this.step4.sessionId = ''
      this.step4.error = ''
      this.step4.status = 'loading'
      this._persist()
    },
    setGeneratedProposals({ proposals, sessionId }) {
      this.step4.proposals = proposals
      this.step4.sessionId = sessionId
      this.step4.error = ''
      this.step4.status = 'success'
      this._persist()
    },
    setProposalError(message) {
      this.step4.proposals = []
      this.step4.selectedTitles = []
      this.step4.error = message
      this.step4.status = 'error'
      this._persist()
    },
    resetStep4() {
      this.step4 = defaultState().step4
      this._persist()
    },

    resetWizard() {
      const fresh = defaultState()
      this.step1 = fresh.step1
      this.step2 = fresh.step2
      this.step3 = fresh.step3
      this.step4 = fresh.step4
      localStorage.removeItem(STORAGE_KEY)
    },

    _persist() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
          step1: this.step1,
          step2: this.step2,
          step3: this.step3,
          step4: this.step4
        }))
      } catch {}
    }
  }
})
