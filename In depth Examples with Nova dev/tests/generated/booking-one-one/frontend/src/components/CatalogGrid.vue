<script setup>
defineProps({
  title: { type: String, required: true },
  rows: { type: Array, default: () => [] },
  fields: { type: Array, default: () => [] },
  canAddToCart: { type: Boolean, default: false }
})

const emit = defineEmits(['add-to-cart'])

function displayName(row) {
  return row.name || row.title || row.productName || 'Item'
}

function displayPrice(row) {
  const value = row.price || row.amount || row.total
  return value === undefined || value === '' ? '' : `$${Number(value).toFixed(2)}`
}
</script>

<template>
  <section class="panel catalog-section">
    <div class="panel-heading">
      <h2>{{ title }}</h2>
      <span>{{ rows.length }} products</span>
    </div>
    <div class="catalog-grid">
      <article v-for="row in rows" :key="row.id || displayName(row)" class="product-card">
        <div>
          <span class="product-kicker">{{ row.category || row.type || 'Product' }}</span>
          <h3>{{ displayName(row) }}</h3>
          <p v-if="row.description">{{ row.description }}</p>
        </div>
        <dl>
          <template v-for="field in fields" :key="field">
            <dt>{{ field }}</dt>
            <dd>{{ row[field] }}</dd>
          </template>
        </dl>
        <div class="product-actions">
          <strong>{{ displayPrice(row) }}</strong>
          <button v-if="canAddToCart" class="primary-button" type="button" @click="emit('add-to-cart', row)">
            Add to Cart
          </button>
        </div>
      </article>
      <p v-if="rows.length === 0" class="empty">No products yet.</p>
    </div>
  </section>
</template>
