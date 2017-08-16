VAGRANTFILE_API_VERSION = "2"


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "tracker", primary: true do |app|
    app.vm.hostname = "tracker"
    app.vm.box = "ubuntu/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh", privileged: false
    app.vm.synced_folder "tracker/", "/home/ubuntu/app"

    app.vm.network "private_network", ip: "192.168.112.10"
  end

  config.vm.define "client-01" do |app|
    app.vm.hostname = "client-01"
    app.vm.box = "ubuntu/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh", privileged: false
    app.vm.synced_folder "client/", "/home/ubuntu/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.11"
  end

  config.vm.define "client-02" do |app|
    app.vm.hostname = "client-02"
    app.vm.box = "ubuntu/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh", privileged: false
    app.vm.synced_folder "client/", "/home/ubuntu/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.12"
  end

  config.vm.define "client-03" do |app|
    app.vm.hostname = "client-03"
    app.vm.box = "ubuntu/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh", privileged: false
    app.vm.synced_folder "client/", "/home/ubuntu/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.13"
  end

  config.vm.define "client-04" do |app|
    app.vm.hostname = "client-04"
    app.vm.box = "ubuntu/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh", privileged: false
    app.vm.synced_folder "client/", "/home/ubuntu/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.14"
  end

  config.vm.define "client-05" do |app|
    app.vm.hostname = "client-05"
    app.vm.box = "ubuntu/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh", privileged: false
    app.vm.synced_folder "client/", "/home/ubuntu/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.15"
  end
end