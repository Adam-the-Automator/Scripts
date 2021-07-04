terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.64.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "avsetdemo-rg"
  location = "westus2"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "snet-logs" {
  name                 = "snet-logs"
  virtual_network_name = azurerm_virtual_network.vnet.name
  resource_group_name  = azurerm_resource_group.rg.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_availability_set" "avset-db" {
  name                         = "avset-db"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  platform_fault_domain_count  = 3
  platform_update_domain_count = 3
  managed                      = true
}

resource "azurerm_network_interface" "nics" {
  count               = 10
  name                = "db0${count.index + 1}-nic"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.snet-logs.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "dbs" {
  count                           = 10
  name                            = "db0${count.index + 1}"
  resource_group_name             = azurerm_resource_group.rg.name
  location                        = azurerm_resource_group.rg.location
  size                            = "Standard_DS1_v2"
  admin_username                  = "adminuser"
  admin_password                  = "N0t@Pa$$word!"
  disable_password_authentication = false
  network_interface_ids = [
    "${azurerm_network_interface.nics.*.id[count.index]}"
  ]
  availability_set_id = azurerm_availability_set.avset-db.id

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "16.04-LTS"
    version   = "latest"
  }
}
