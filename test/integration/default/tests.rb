describe package('epel-release') do
  it { should be_installed }
end
    
describe package('python2-pip') do
  it { should be_installed }
end
    
describe pip('pip') do
  it { should be_installed }
  its('version') { should cmp >= '19.1.1' }
end
    
describe pip('ansible') do
  it { should be_installed }
  its('version') { should eq '2.7.10' }
end
