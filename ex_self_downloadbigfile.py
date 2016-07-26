def download(self, url, filename, headers = {}):
        finished = False
        block = self.config['block']
        local_filename = self.remove_nonchars(filename)
        tmp_filename = local_filename + '.downtmp'
        if self.support_continue(url):  # 支持断点续传
                try:
                        with open(tmp_filename, 'rb') as fin:
                                self.size = int(fin.read()) + 1
                except:
                        self.touch(tmp_filename)
                finally:
                        headers['Range'] = "bytes=%d-" % (self.size, )
        else:
                self.touch(tmp_filename)
                self.touch(local_filename)

        size = self.size
        total = self.total
        r = requests.get(url, stream = True, verify = False, headers = headers)
        if total > 0:
                print "[+] Size: %dKB" % (total / 1024)
        else:
                print "[+] Size: None"
        start_t = time.time()
        with open(local_filename, 'ab') as f:
                try:
                        for chunk in r.iter_content(chunk_size = block): 
                                if chunk:
                                        f.write(chunk)
                                        size += len(chunk)
                                        f.flush()
                                sys.stdout.write('\b' * 64 + 'Now: %d, Total: %s' % (size, total))
                                sys.stdout.flush()
                        finished = True
                        os.remove(tmp_filename)
                        spend = int(time.time() - start_t)
                        speed = int(size / 1024 / spend)
                        sys.stdout.write('\nDownload Finished!\nTotal Time: %ss, Download Speed: %sk/s\n' % (spend, speed))
                        sys.stdout.flush()

                except:
                        import traceback
                        print traceback.print_exc()
                        print "\nDownload pause.\n"
                finally:
                        if not finished:
                                with open(tmp_filename, 'wb') as ftmp:
                                        ftmp.write(str(size))