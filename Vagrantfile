VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "tracker", primary: true do |app|
    app.vm.hostname = "tracker"
    app.vm.box = "minimal/xenial64"

    app.vm.provision "shell", path: "tracker/scripts/bootstrap.sh"
    app.vm.synced_folder "tracker/", "/home/vagrant/app"

    app.vm.network "private_network", ip: "192.168.112.1"

    app.trigger.after :up do
      run "vagrant ssh tracker -c '/home/vagrant/app/scripts/server.sh' -- -n"
    end
  end

  config.vm.define "app_01" do |app|
    app.vm.hostname = "app_01"
    app.vm.box = "minimal/xenial64"

    app.vm.provision "shell", path: "client/scripts/bootstrap.sh"
    app.vm.synced_folder "client/", "/home/vagrant/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.2"

    app.trigger.after :up do
      run "vagrant ssh app_01 -c '/home/vagrant/app/scripts/server.sh' -- -n"
    end
  end

  config.vm.define "app_02" do |app|
    app.vm.hostname = "app_02"
    app.vm.box = "minimal/xenial64"

    app.vm.provision "shell", path: "client/scripts/bootstrap.sh"
    app.vm.synced_folder "client/", "/home/vagrant/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.2"

    app.trigger.after :up do
      run "vagrant ssh app_02 -c '/home/vagrant/app/scripts/server.sh' -- -n"
    end
  end

  config.vm.define "app_03" do |app|
    app.vm.hostname = "app_03"
    app.vm.box = "minimal/xenial64"

    app.vm.provision "shell", path: "client/scripts/bootstrap.sh"
    app.vm.synced_folder "client/", "/home/vagrant/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.3"

    app.trigger.after :up do
      run "vagrant ssh app_03 -c '/home/vagrant/app/scripts/server.sh' -- -n"
    end
  end

  config.vm.define "app_04" do |app|
    app.vm.hostname = "app_04"
    app.vm.box = "minimal/xenial64"

    app.vm.provision "shell", path: "client/scripts/bootstrap.sh"
    app.vm.synced_folder "client/", "/home/vagrant/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.4"

    app.trigger.after :up do
      run "vagrant ssh app_04 -c '/home/vagrant/app/scripts/server.sh' -- -n"
    end
  end

  config.vm.define "app_05" do |app|
    app.vm.hostname = "app_05"
    app.vm.box = "minimal/xenial64"

    app.vm.provision "shell", path: "client/scripts/bootstrap.sh"
    app.vm.synced_folder "client/", "/home/vagrant/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.5"

    app.trigger.after :up do
      run "vagrant ssh app_05 -c '/home/vagrant/app/scripts/server.sh' -- -n"
    end
  end
end