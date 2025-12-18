@description('Location for all resources')
param location string = 'westeurope'

@description('Name of the Azure Container Registry')
param acrName string = 'projektrdevopsacr'

@description('Name of the Resource Group')
param rgName string = 'projektrdevops-rg'

resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: rgName
  location: location
}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: acrName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}
