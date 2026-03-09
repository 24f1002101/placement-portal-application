<script setup>
import { ref, onMounted } from 'vue';
import { companyStore } from '@/stores/company_store';
import { computed } from 'vue';

const emit = defineEmits(['action-taken'])
const company_store = companyStore()
const props = defineProps({
    searchResults: Array,
    searchType: String
})
const approved_list = computed(() => {
    if (props.searchType !== 'company') return []
    return props.searchResults.filter(c => c.status === 'approved')
})
const pending_companies = computed(() => {
    if (props.searchType !== 'company') return []
    return props.searchResults.filter(c => c.status === 'pending')
})

async function handleBlacklist(companyId) {
    const success = await company_store.black_list(companyId)
    if (success) emit('action-taken', companyId)
}

async function handleApprove(companyId) {
    const success = await company_store.approve_company(companyId)
    if (success) emit('action-taken', companyId)
}

onMounted(async () => {
    await company_store.fetchapprovedCompanies()
    await company_store.fetchpendingCompanies()
})
</script>

<template>
    <div class="container-fluid py-4 px-4 bg-light min-vh-100">
        
        <div class="card border-0 shadow-sm mb-5">
            <div class="card-header bg-white border-bottom py-3 d-flex align-items-center justify-content-between">
                <h2 class="h5 mb-0 fw-bold text-dark" v-if="!company_store.error_value">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>Registered Companies
                </h2>
                <span class="badge bg-primary rounded-pill" v-if="searchType === 'company'">Search Results</span>
            </div>
            
            <div class="card-body p-0">
                <div v-if="searchType === 'company' && approved_list.length">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th class="ps-4">Company Name</th>
                                    <th class="text-end pe-4">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="company in approved_list" :key="company.company_id">
                                    <td class="ps-4 fw-medium">{{ company.company_name }}</td>
                                    <td class="text-end pe-4">
                                        <button class="btn btn-outline-danger btn-sm px-3" @click="handleBlacklist(company.company_id)">
                                            Blacklist
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div v-else>
                    <div v-if="company_store.approvedCompanies.length === 0 && !company_store.error_value" class="p-5 text-center">
                        <div class="text-muted mb-2 fs-4">Empty List</div>
                        <p class="text-secondary small">No registered companies found in the database.</p>
                    </div>
                    <div v-else class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th class="ps-4">Company Name</th>
                                    <th class="text-end pe-4">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="company in company_store.approvedCompanies" :key="company.company_id">
                                    <td class="ps-4 fw-medium">{{ company.company_name }}</td>
                                    <td class="text-end pe-4">
                                        <button class="btn btn-outline-danger btn-sm px-3" @click="company_store.black_list(company.company_id)">
                                            Blacklist
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom py-3">
                <h2 class="h5 mb-0 fw-bold text-dark" v-if="!company_store.error_value">
                    <i class="bi bi-clock-history text-warning me-2"></i>Pending Approvals
                </h2>
            </div>
            
            <div class="card-body p-0">
                <div v-if="searchType === 'company' && pending_companies.length">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th class="ps-4">Company Name</th>
                                    <th class="text-end pe-4">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="company in pending_companies" :key="company.company_id">
                                    <td class="ps-4 fw-medium">{{ company.company_name }}</td>
                                    <td class="text-end pe-4">
                                        <button class="btn btn-success btn-sm px-4 shadow-sm" @click="handleApprove(company.company_id)">
                                            Approve
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div v-else>
                    <div v-if="company_store.pendingCompanies.length === 0 && !company_store.error_value" class="p-5 text-center">
                        <div class="text-muted mb-2 fs-4">All Caught Up!</div>
                        <p class="text-secondary small">There are no companies awaiting approval.</p>
                    </div>
                    <div v-else class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th class="ps-4">Company Name</th>
                                    <th class="text-end pe-4">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="company in company_store.pendingCompanies" :key="company.company_id">
                                    <td class="ps-4 fw-medium">{{ company.company_name }}</td>
                                    <td class="text-end pe-4">
                                        <button class="btn btn-success btn-sm px-4 shadow-sm" @click="company_store.approve_company(company.company_id)">
                                            Approve
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<style scoped>
/* Adding a little extra finesse that Bootstrap utilities alone sometimes miss */
.table thead th {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
    color: #6c757d;
}

.card {
    border-radius: 12px;
    overflow: hidden;
}

.btn-sm {
    border-radius: 8px;
    font-weight: 500;
}
</style>