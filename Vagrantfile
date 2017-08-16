VAGRANTFILE_API_VERSION = "2"


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "blockchain-tracker", primary: true do |app|
    app.vm.hostname = "blockchain-tracker"
    app.vm.box = "ubuntu/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh", privileged: false
    app.vm.synced_folder "tracker/", "/home/ubuntu/app"

    app.vm.network "private_network", ip: "192.168.112.10"
  end

  for index in 1..5
    server_name = "blockchain-client-%s" % index
    config.vm.define server_name do |app|
      app.vm.hostname = server_name
      app.vm.box = "ubuntu/xenial64"

      app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh", privileged: false
      app.vm.synced_folder "client/", "/home/ubuntu/app"

      app.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "512"]
      end

      app.vm.network "private_network", ip: "192.168.112.1#{index}"
    end
  end

end