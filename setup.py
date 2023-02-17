from io import StringIO
import paramiko


class SshClient:
    "A wrapper of paramiko.SSHClient"
    TIMEOUT = 4

    def __init__(self, host, username, password, key=None, passphrase=None):
        self.username = username
        self.password = password
        # creating an object of the SSHClient.
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key is not None:
            key = paramiko.RSAKey.from_private_key(StringIO(key), password=passphrase)
        # Establishing connection with the given host details.
        self.client.connect(host, username=username, password=password, pkey=key, timeout=self.TIMEOUT)

    def close(self):
        # closing the connection with the sshclient after the command execution is completed.
        if self.client is not None:
            self.client.close()
            self.client = None

    def execute(self, command, sudo=False):
        feed_password = False
        if sudo and self.username != "root":
            command = "sudo -S -p '' %s" % command
            # print(command)
            feed_password = self.password is not None and len(self.password) > 0
        stdin, stdout, stderr = self.client.exec_command(command)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()
        return {'out': stdout.readlines(),
                'err': stderr.readlines(),
                'retval': stdout.channel.recv_exit_status()}

    def load_docker_file(self):
        client = SshClient(host='192.168.5.12', username='nihar', password='@four123')
        try:
            text_file = open("docker-compose.yml", "r")
            # read whole file to a string
            data = text_file.read()
            # close file
            text_file.close()
            ret = client.execute('echo "' + data + '">> docker-compose.yml', sudo=True)
            print("  ".join(ret["out"]), ret["retval"])
        finally:
            client.close()

    def install_docker(self):
        self.client = SshClient(host='192.168.5.12', username='nihar', password='@four123')
        try:
            ret = client.execute('apt install docker.io -y', sudo=True)
            print("  ".join(ret["out"]), ret["retval"])
        finally:
            client.close()
        # To-Do:
        # Scaling --> docker-compose scale chrome=3


if __name__ == "__main__":
    client = SshClient(host='192.168.5.12', username='nihar', password='@four123')
    try:
        ret = client.execute('docker-compose up', sudo=True)
        print("  ".join(ret["out"]), ret["retval"])
    finally:
        client.close()
