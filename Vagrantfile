VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "tracker", primary: true do |app|
    app.vm.hostname = "tracker"
    app.vm.box = "minimal/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh"
    app.vm.synced_folder "tracker/", "/home/vagrant/app"

    app.vm.network "private_network", ip: "192.168.112.10"

    app.vm.provision :shell, path: "deploy/scripts/runserver.sh", run: 'always'
  end

  config.vm.define "app_01" do |app|
    app.vm.hostname = "app_01"
    app.vm.box = "minimal/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh"
    app.vm.synced_folder "client/", "/home/vagrant/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.11"

    app.trigger.after :up do
      run "vagrant ssh app_01 -c 'deploy/scripts/runserver.sh' -- -n"
    end
  end

  config.vm.define "app_02" do |app|
    app.vm.hostname = "app_02"
    app.vm.box = "minimal/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh"
    app.vm.synced_folder "client/", "/home/vagrant/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.12"

    app.trigger.after :up do
      run "vagrant ssh app_02 -c 'deploy/scripts/runserver.sh' -- -n"
    end
  end

  config.vm.define "app_03" do |app|
    app.vm.hostname = "app_03"
    app.vm.box = "minimal/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh"
    app.vm.synced_folder "client/", "/home/vagrant/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.13"

    app.trigger.after :up do
      run "vagrant ssh app_03 -c 'deploy/scripts/runserver.sh' -- -n"
    end
  end

  config.vm.define "app_04" do |app|
    app.vm.hostname = "app_04"
    app.vm.box = "minimal/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh"
    app.vm.synced_folder "client/", "/home/vagrant/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.14"

    app.trigger.after :up do
      run "vagrant ssh app_04 -c 'deploy/scripts/runserver.sh' -- -n"
    end
  end

  config.vm.define "app_05" do |app|
    app.vm.hostname = "app_05"
    app.vm.box = "minimal/xenial64"

    app.vm.provision "shell", path: "deploy/scripts/bootstrap.sh"
    app.vm.synced_folder "client/", "/home/vagrant/app"

    app.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
    end

    app.vm.network "private_network", ip: "192.168.112.15"

    app.trigger.after :up do
      run "vagrant ssh app_05 -c 'deploy/scripts/runserver.sh' -- -n"
    end
  end
end